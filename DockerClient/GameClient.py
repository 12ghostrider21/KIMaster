import asyncio
import json

import websockets


class GameClient:
    def __init__(self, host: str, port: int, key: str):
        self.host: str = host
        self.port: int = port
        self.websocket = None
        self.key: str = key

    async def connect(self):
        url = f"ws://{self.host}:{self.port}/ws"
        try:
            self.websocket = await websockets.connect(url, ping_interval=None)
            message = await self.receive_message()
            if message == "No Lobby":
                return False
            self.key = json.loads(message).get("key")
            return True
        except ConnectionRefusedError as e:
            print(f"Can not connect to SocketServer {url}. Closing")
            return False

    async def send_message(self, message):
        try:
            await self.websocket.send(message)
        except AttributeError:
            print(f"{message=} is not a str or bytes or iterable!")
        print(f"Sent message: {message}")

    async def receive_json(self):
        json_string = await self.receive_message()
        if json_string is None:
            return None
        return json.loads(json_string)

    async def receive_message(self):
        try:
            response = await self.websocket.recv()
            print(f"Received message: {response}")
            return response
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed.")

    async def run(self):
        loop = await self.connect()
        while loop:
            # Send a message
            message = input("Type your message (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            if message == "key":
                print(self.key)
            await self.send_message(message)
            response = await self.receive_message()
        await self.websocket.close()
