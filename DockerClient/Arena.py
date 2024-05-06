from GameClient import GameClient
from Pit import Pit


class Arena(GameClient, Pit):
    def __init__(self, host: str, port: int):
        GameClient.__init__(self, host, port)
        Pit.__init__(self)

    async def readLoop(self):
        await self.connect()

        while True:
            # Send a message
            message = input("Type your message (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break

            if message == "t":
                self.test()

            if message == "ta":
                self.testArena()

            await self.send_message(message)

            # Receive response
            response = await self.receive_message()

        # Close the WebSocket connection
        await self.websocket.close()
        print("WebSocket connection closed.")

    def testArena(self):
        print("Test in Arena")
