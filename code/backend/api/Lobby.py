from dataclasses import dataclass
from starlette.websockets import WebSocket
from typing import Set

@dataclass
class Lobby:
    clients = []
    viewer = []

    def addClient(self, websocket: WebSocket) -> bool:
        if len(self.clients) < 2:
            self.clients.append(websocket)
            return True
        return False
