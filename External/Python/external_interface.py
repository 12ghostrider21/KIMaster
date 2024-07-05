# external_interface.py
import asyncio
import json
from abc import ABC, abstractmethod
from typing import Coroutine

import websockets
from websockets.exceptions import InvalidStatusCode, ConnectionClosedOK, ConnectionClosedError

__all__ = ["Interface"]


class Interface(ABC):
    def __init__(self, host: str, port: int):
        self._host: str = host
        self._port: int = port
        self._websocket = None

    async def connect(self):
        uri = f"ws://{self._host}:{self._port}/ws"
        while not self._websocket:
            try:
                self._websocket = await websockets.connect(uri, ping_interval=20, ping_timeout=20)
                print("\nSuccessfully connected.\n")
                return True
            except (InvalidStatusCode, ConnectionRefusedError) as e:
                print(f"Connection error: {e}. Retrying in 5 seconds...")
                await asyncio.sleep(5)
        return False

    async def disconnect(self):
        if self._websocket:
            await self._websocket.close()
            self._websocket = None
            print("\nDisconnected successfully.\n")

    async def connected(self) -> bool:
        return self._websocket is not None and not self._websocket.closed

    async def send_cmd(self, command: str, command_key: str, data: dict = None):
        if await self.connected():
            cmd = {"command": command, "command_key": command_key}
            if data:
                cmd.update(data)
            await self._websocket.send(json.dumps(cmd))

    async def receive(self) -> dict | bytes:
        if await self.connected():
            received = {}
            try:
                received = await self._websocket.recv()
                return json.loads(received)
            except (ConnectionClosedOK, ConnectionClosedError) as e:
                print(f"Connection closed: {e}")
                await self.disconnect()
                return received
            except json.decoder.JSONDecodeError:
                return received

    def start(self, target: Coroutine):
        asyncio.run(target)

    @abstractmethod
    async def main(self, *args, **kwargs):
        pass