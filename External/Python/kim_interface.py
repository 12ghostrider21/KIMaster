import asyncio
import json
from abc import ABC
import io

from PIL import Image
from websockets import WebSocketClientProtocol, connect, InvalidURI, ConnectionClosedOK


class KIMaster(ABC):
    def __init__(self, uri_pool: list[str]):
        self.connection: WebSocketClientProtocol | None = None
        self.uri_pool: list[str] = uri_pool

    async def connect(self):
        for uri in self.uri_pool:
            print(f"Try to connect to URI: '{uri}'")
            try:
                self.connection: WebSocketClientProtocol = await connect(uri)
                print(f"Connected to URI: '{uri}'")
                break
            except InvalidURI:
                print(f"URI: '{uri}' not reachable!")

    async def send_cmd(self, command: str, command_key: str, data: dict = None):
        if self.connection:
            payload: dict = {"command": command, "command_key": command_key}
            if data is not None:
                payload.update(data)
            await self.connection.send(json.dumps(payload))

    async def receive(self):
        if self.connection:
            message = None
            try:
                message = await self.connection.recv()
            except ConnectionClosedOK:
                return
            try:
                data = json.loads(message)
                return data
            except json.JSONDecodeError:
                # Handle binary data (e.g., PNG bytestream)
                return message
            except UnicodeDecodeError:
                return message

    async def close(self):
        if self.connection:
            await self.connection.close()

    def run(self, target):
        asyncio.run(target)

    async def handler(self, send_handler, receive_handler):
        # Create tasks for both handlers
        send_task = asyncio.create_task(send_handler())
        receive_task = asyncio.create_task(receive_handler())

        # Wait for both tasks to complete
        await asyncio.gather(send_task, receive_task)

    def print_message(self, message: dict):
        print("\n")
        for k, v in message.items():
            print(f" -- {k}: {v}")

    def show(self, message: bytes):
        image_stream = io.BytesIO(message)
        image = Image.open(image_stream)

        # Display the image
        image.show()
