import websockets


class GameClient:
    def __init__(self, host: str, port: int):
        self.host: str = host
        self.port: int = port
        self.websocket = None

    async def connect(self):
        url = f"ws://{self.host}:{self.port}/ws"
        self.websocket = await websockets.connect(url, close_timeout=None)
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