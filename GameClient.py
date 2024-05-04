import asyncio
import websockets

class GameClient:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self.receive_task = None

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.uri)
            print(f"Connected to {self.uri}")
            self.receive_task = asyncio.create_task(self.receive())
        except ConnectionRefusedError:
            print(f"Failed to connect to {self.uri}")

    async def receive(self):
        try:
            while True:
                message = await self.websocket.recv()
                print(f"Received: {message}")
        except websockets.ConnectionClosed:
            print("Connection to server closed.")

    async def send_msg(self, data):
        await self.websocket.send(data)
