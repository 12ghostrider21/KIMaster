from external_interface import Interface


class Example(Interface):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)

    async def main(self):
        connected = await self.connect()
        while connected:
            result = await self.send_receive("lobby", "create")
            print(result)
            result = await self.send_receive("lobby", "status")
            print(result)
            break


e = Example("localhost", 8000)
e.start(e.main())
