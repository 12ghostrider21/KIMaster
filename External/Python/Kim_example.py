import asyncio
import json
import threading
from queue import Queue
from kim_interface import KIMaster


class Example(KIMaster):
    def __init__(self, uri_list: list[str]):
        super().__init__(uri_list)
        self.command_queue = Queue()

        self.exit = False

    def input_thread(self):
        while not self.exit:
            command = input("Command: ")
            if command == "exit":
                self.exit = True
                break
            command_key = input("Command_key: ")
            data = input("Data")
            if data == "":
                data = None
            else:
                data = json.loads(data)
            self.command_queue.put((command, command_key, data))

    async def send_handler(self):
        while not self.exit:
            if not self.command_queue.empty():
                command, command_key, data = self.command_queue.get()
                await self.send_cmd(command, command_key, data)
            await asyncio.sleep(0.1)    # needed to jump between tasks
        await self.close()

    async def receive_handler(self):
        while not self.exit:
            message = await self.receive()
            if isinstance(message, dict):
                self.print_message(message)
            if isinstance(message, bytes):
                self.show(message)
        await self.close()

    async def main(self):
        await self.connect()

        # Start the input thread
        input_thread = threading.Thread(target=self.input_thread, daemon=True)
        input_thread.start()

        # link both methods to oen asyncio tasks
        await self.handler(self.send_handler, self.receive_handler)


if __name__ == "__main__":
    uri = ["wss:/kimaster.mni.thm.de/ws", "ws://localhost:8010/ws"]
    master = Example(uri_list=uri)
    master.run(master.main())
