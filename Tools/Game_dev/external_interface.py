import asyncio
import json
from abc import ABC, abstractmethod

import websockets
from websockets.exceptions import InvalidStatusCode


class Interface(ABC):
    def __init__(self, host: str, port: int):
        self._host: str = host
        self._port: int = port
        self._websocket = None

    async def connect(self):
        uri = f"ws://{self._host}:{self._port}/ws"
        try:
            self._websocket = await websockets.connect(uri, ping_interval=None)
            print("\nSuccessfully connected.\n")
            return True
        except InvalidStatusCode as e:
            print(e)
            return False
        except ConnectionRefusedError as e:
            print(f"Cannot connect to server with: {uri}")
            return False

    async def disconnect(self):
        if self._websocket:
            await self._websocket.close()
            self._websocket = None
            print("\nDisconnected successfully.\n")

    async def connected(self) -> bool:
        if self._websocket:
            return True
        raise ConnectionError("Not connected to a WebSocket")

    async def __send_cmd(self, command: str, command_key: str, data: dict = None):
        if await self.connected():
            cmd = {"command": command, "command_key": command_key}
            if data:
                cmd.update(data)
            print(f"Sent cmd: {cmd}")
            await self._websocket.send(json.dumps(cmd))

    async def __receive(self) -> dict | bytes:
        if await self.connected():
            received = await self._websocket.recv()
            try:
                return json.loads(received)
            except json.decoder.JSONDecodeError:
                return bytes(received)

    async def send_receive(self, command: str, command_key: str, data: dict = None) -> dict | bytes:
        await self.__send_cmd(command, command_key, data)
        return await self.__receive()

    def start(self, target: callable):
        asyncio.run(target)

    @abstractmethod
    async def main(self, *args, **kwargs):
        pass
