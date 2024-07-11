import asyncio
import json
from abc import ABC
import io
from typing import Coroutine
from PIL import Image
from websockets import WebSocketClientProtocol, connect, InvalidURI, ConnectionClosedOK


class KIMaster(ABC):
    def __init__(self, uri_pool: list[str]):
        """
        Initialize the KIMaster with a list of URIs.

        :param uri_pool: List of URIs to connect to.
        """
        # WebSocket connection instance
        self.connection: WebSocketClientProtocol | None = None
        # Pool of URIs to attempt connection with
        self.uri_pool: list[str] = uri_pool

    async def connect(self) -> None:
        """
        Try to connect to one of the URIs in the uri_pool.
        """
        for uri in self.uri_pool:
            print(f"Try to connect to URI: '{uri}'")
            try:
                # Attempt to establish a WebSocket connection
                self.connection = await connect(uri)
                print(f"Connected to URI: '{uri}'")
                break
            except InvalidURI:
                # Handle invalid URI exception
                print(f"URI: '{uri}' not reachable!")

    async def send_cmd(self, command: str, command_key: str, data: dict | None = None) -> None:
        """
        Send a command to the connected WebSocket server.

        :param command: The command to send.
        :param command_key: The command key associated with the command.
        :param data: Optional additional data to send with the command.
        """
        if self.connection:
            # Prepare payload with command and command_key
            payload: dict = {"command": command, "command_key": command_key}
            if data is not None:
                # Add additional data if provided
                payload.update(data)
            # Send payload as JSON string
            await self.connection.send(json.dumps(payload))

    async def receive(self) -> dict | str | bytes | None:
        """
        Receive a message from the WebSocket server.

        :return: The received message, either as a dictionary, string, or bytes.
        """
        if self.connection:
            message = None
            try:
                # Attempt to receive a message
                message = await self.connection.recv()
            except ConnectionClosedOK:
                return
            try:
                # Try to parse the message as JSON
                data = json.loads(message)
                return data
            except json.JSONDecodeError:
                # Handle binary data (e.g., PNG bytestream)
                return message
            except UnicodeDecodeError:
                # Handle non-UTF-8 encoded data
                return message

    async def close(self) -> None:
        """
        Close the WebSocket connection.
        """
        if self.connection:
            # Close the WebSocket connection
            await self.connection.close()

    def run(self, target: Coroutine) -> None:
        """
        Run the given coroutine until it completes.

        :param target: The coroutine to run.
        """
        # Run the given coroutine
        asyncio.run(target)

    async def handler(self, send_handler, receive_handler) -> None:
        """
        Handle both sending and receiving of WebSocket messages.

        :param send_handler: The coroutine handling sending messages.
        :param receive_handler: The coroutine handling receiving messages.
        """
        # Create tasks for both handlers
        send_task = asyncio.create_task(send_handler())
        receive_task = asyncio.create_task(receive_handler())

        # Wait for both tasks to complete
        await asyncio.gather(send_task, receive_task)

    def print_message(self, message: dict) -> None:
        """
        Print a formatted message to the console.

        :param message: The message to print.
        """
        print("\n")
        for k, v in message.items():
            # Print each key-value pair in the message
            print(f" -- {k}: {v}")

    def show(self, message: bytes) -> None:
        """
        Display an image from a byte stream.

        :param message: The image data as bytes.
        """
        # Convert byte stream to an image
        image_stream = io.BytesIO(message)
        image = Image.open(image_stream)

        # Display the image
        image.show()
