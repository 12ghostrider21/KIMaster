import asyncio
from dataclasses import dataclass, field
from external_interface import Interface

@dataclass
class Entry:
    command: str = field(default="")
    command_key: str = field(default="")
    data: dict = field(default_factory=dict)

    def __str__(self):
        return f"{self.command} - {self.command_key}{'' if self.data == {} else self.data.__str__()}"


class Example(Interface):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)
        self.key = ""

    async def main(self):
        connected = await self.connect()
        if not connected:
            return

        # Start the tasks for receiving messages and sending commands
        send_task = asyncio.create_task(self.send_commands())
        receive_task = asyncio.create_task(self.receive_messages())

        # Wait for both tasks to finish (which they never will in a while True loop)
        await asyncio.gather(receive_task, send_task)

    def get_commands(self) -> dict[str, Entry]:
        return {"0": Entry("lobby", "status"),
                "1": Entry("lobby", "pos"),
                "2": Entry("lobby", "create"),
                "3": Entry("lobby", "leave"),
                "4": Entry("lobby", "games")}

    async def receive_messages(self):
        while await self.connected():
            message = await self.receive()
            if message:
                if "key" in message:
                    self.key = message.get("key")
                print("\nReceived:")
                for k, v in message.items():
                    print(f" -- {k}: {v}")

    async def send_commands(self):
        loop = asyncio.get_running_loop()

        while await self.connected():
            command = self.get_commands()   # updates every time
            for k,v in command.items():
                print(f"[{k}] : {v}")
            # Use a thread to handle the blocking input call
            user_input = await loop.run_in_executor(None, input, "Enter command: ")
            if user_input == "-1":
                await self.disconnect()
            if user_input in command.keys():
                x = command.get(user_input)
                await self.send_cmd(command=x.command,
                                    command_key=x.command_key,
                                    data=x.data)


if __name__ == "__main__":
    e = Example(host="localhost", port=8000)
    e.start(e.main())
