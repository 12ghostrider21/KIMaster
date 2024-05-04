import asyncio
import websockets


class GameClient:
    def __init__(self, host: str, port: int):
        self.host: str = host
        self.port: int = port
        self.websocket = None

    async def connect(self):
        url = f"ws://{self.host}:{self.port}/ws"
        self.websocket = await websockets.connect(url)
        print(f"Connected to {url}")

    async def send_message(self, message):
        await self.websocket.send(message)
        print(f"Sent message: {message}")

    async def receive_message(self):
        try:
            response = await self.websocket.recv()
            print(f"Received message: {response}")
            return response
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed.")

    async def run(self):
        await self.connect()

        while True:
            # Send a message
            message = input("Type your message (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break

            await self.send_message(message)

            # Receive response
            response = await self.receive_message()

        # Close the WebSocket connection
        await self.websocket.close()
        print("WebSocket connection closed.")


if __name__ == "__main__":

    # Create and run the WebSocketClient instance
    client = GameClient("localhost", 12345)
    asyncio.run(client.run())
