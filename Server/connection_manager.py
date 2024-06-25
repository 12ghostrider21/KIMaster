from abc import ABC, abstractmethod
from fastapi import WebSocket
from Tools.language_handler import LanguageHandler
from Tools.languages import LANGUAGE
from Tools.rcode import RCODE


class AbstractConnectionManager(ABC):
    """
    Abstract base class for managing WebSocket connections.

    Attributes:
        active_connections (list[WebSocket]): List to store active WebSocket connections.
        msg_builder (LanguageHandler): Instance to handle language-specific messages.
        language (LANGUAGE): Default language for the connection manager.
    """

    def __init__(self, msg_builder: LanguageHandler):
        """
        Initialize the connection manager with a language handler.

        Args:
            msg_builder (LanguageHandler): Language handler instance.
        """
        self.active_connections: list[WebSocket] = []
        self.msg_builder: LanguageHandler = msg_builder
        self.language: LANGUAGE = LANGUAGE.EN

    @abstractmethod
    async def connect(self, websocket: WebSocket):
        """
        Abstract method to handle new WebSocket connections.

        Args:
            websocket (WebSocket): The WebSocket connection to be added.
        """
        pass

    @abstractmethod
    async def disconnect(self, websocket: WebSocket):
        """
        Abstract method to handle WebSocket disconnections.

        Args:
            websocket (WebSocket): The WebSocket connection to be removed.
        """
        pass

    async def send_bytes(self, client: WebSocket, data: bytes):
        """
        Send binary data to a WebSocket client.

        Args:
            client (WebSocket): The WebSocket client.
            data (bytes): The binary data to be sent.
        """
        if client is not None:
            await client.send_bytes(data)

    async def send_response(self, client: WebSocket, code: RCODE, data: dict | None = None):
        """
        Send a response message to a WebSocket client.

        Args:
            client (WebSocket): The WebSocket client.
            code (RCODE): Response code.
            data (dict, optional): Additional data to be included in the response.
        """
        if client is None:
            return
        cmd = {
            "response_code": code.value,
            "response_msg": self.msg_builder.get(code.value, self.language.name.lower())
        }
        if data:
            cmd.update(data)
        await client.send_json(cmd)

    async def broadcast_response(self, client_list: list[WebSocket], code: RCODE, data: dict | None = None):
        """
        Broadcast a response message to multiple WebSocket clients.

        Args:
            client_list (list[WebSocket]): List of WebSocket clients.
            code (RCODE): Response code.
            data (dict, optional): Additional data to be included in the response.
        """
        for c in client_list:
            if c is not None:
                await self.send_response(c, code, data)

    async def send_cmd(self, game_client: WebSocket, command: str, command_key: str, data: dict = None):
        """
        Send a command to a game client.

        Args:
            game_client (WebSocket): The WebSocket client.
            command (str): The command to be sent.
            command_key (str): The command key.
            data (dict, optional): Additional data to be included in the command.
        """
        cmd = {"command": command, "command_key": command_key}
        if data is not None:
            cmd.update(data)
        await game_client.send_json(cmd)
