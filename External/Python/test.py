from typing import Any
import asyncio
from external_interface import Interface

class KI(Interface):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)
    

    async def main(self):
        connected = await self.connect()
        print(connected)
        if not connected:
            return

        await self.disconnect()


if __name__ == "__main__":
    x = KI("localhost", 8010)
    x.start(x.main())

