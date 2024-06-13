from abc import ABC, abstractmethod
from fastapi import WebSocket

from Server.lobby import Lobby
from Tools.language_handler import LanguageHandler
from Tools.rcode import RCODE
from Tools.languages import LANGUAGE


class AbstractConnectionManager(ABC):
    def __init__(self, msg_builder: LanguageHandler):
        self.active_connections: list[WebSocket] = []
        self.msg_builder: LanguageHandler = msg_builder
        self.language: LANGUAGE = LANGUAGE.EN

    @abstractmethod
    async def connect(self, websocket: WebSocket):
        pass

    @abstractmethod
    async def disconnect(self, websocket: WebSocket):
        pass

    async def send_bytes(self, client: WebSocket, data: bytes):
        if client is not None:
            await client.send_bytes(data)

    async def send_response(self, client: WebSocket, code: RCODE, data: dict | None = None):
        if client is None:
            return
        cmd = {"response_code:": code.value, "response_msg": self.msg_builder.get(code.value, self.language.name.lower())}
        if data:
            cmd.update(data)
        await client.send_json(cmd)

    async def broadcast_response(self, client_list: list[WebSocket], code: RCODE, data: dict | None = None):
        for c in client_list:
            if c is not None:
                await self.send_response(c, code, data)

    async def send_cmd(self, game_client: WebSocket, command: str, command_key: str, data: dict = None):
        """
        Send a command to a game client.
        """
        cmd = {"command": command, "command_key": command_key}
        if data is not None:
            cmd.update(data)
        await game_client.send_json(cmd)
