import hashlib
from datetime import datetime, timezone
from json.decoder import JSONDecodeError
from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketState, WebSocketDisconnect
from Lobby import Lobby
from Datatypes import EGame
from pygame import surface


class SocketServer:
    def __init__(self):
        self.__app = FastAPI()
        self.lobbies: dict[str, Lobby] = {}

        @self.__app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await self.connect(websocket)
            while True:
                try:
                    readObject = await websocket.receive_text()
                    print(readObject)
                    await websocket.send_text(readObject)
                except WebSocketDisconnect:
                    print("websocket closes...")
                    break
            await self.disconnect(websocket)

    # *************************************************************************************************************
    # Lobby
    def _generate_lobby_key(self) -> str:
        current_time = datetime.now(timezone.utc).timestamp()  # Get the current date and time as a Unix timestamp
        time_str = str(current_time)  # Convert the timestamp to a string
        time_bytes = time_str.encode('utf-8')  # Encode the string to bytes using UTF-8
        sha256_hash = hashlib.sha256(time_bytes)  # Calculate the SHA256 hash of the bytes
        hex_digest = sha256_hash.hexdigest()  # Get the hexadecimal representation of the hash as a string
        if hex_digest in self.lobbies.keys():
            return self._generate_lobby_key()
        return hex_digest

    def new_lobby(self, client: WebSocket):
        for lobby in self.lobbies.values():
            if lobby.client_in_lobby(client):
                return f"Client in Lobby {lobby.key} creation failed!", None
        key = self._generate_lobby_key()
        self.lobbies[key] = Lobby(key)
        return f"New Lobby with {key=} created!", key

    def lobby_exist(self, key) -> bool:
        if key is None:
            return False
        return key in self.lobbies.keys()

    def join_lobby(self, key: str, client: WebSocket) -> str:
        lobby = self.lobbies.get(key)
        if lobby:
            return lobby.join(client)
        return "Lobby does not exist!"

    def leave_lobby(self, key: str, client: WebSocket) -> str:
        lobby = self.lobbies.get(key)
        if lobby is None:
            return "Lobby does not exist!"
        msg = lobby.leave(client)
        return msg

    def load_game(self, key: str, game_name):
        for game in EGame:
            if game.name == game_name:
                lobby = self.lobbies.get(key)
                if lobby is None:
                    return "Lobby does not exits!"
                if lobby.game is not None:
                    return "Game is running, cant change!"
                lobby.game = game
                return f"Game {game.name} set in lobby {key}"
        return f"Game with name: {game_name} not available!"

    def get_lobby_key_of_client(self, client: WebSocket) -> str | None:
        """
        :param client: a Websocket from FastAPIServer
        :return: key or None on not found!
        """
        for lobby in self.lobbies.values():
            if lobby.client_in_lobby(client):
                return lobby.key
        return None

    # *************************************************************************************************************

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        print(f"GameClient connected with: {websocket}")

    async def send_image(self, image_bytes: bytes, websocket: WebSocket):
        await websocket.send_bytes(image_bytes)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def disconnect(self, websocket: WebSocket):
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.close(code=1000, reason="Server initiated closure")
        print(f"GameClient disconnected with: {websocket}")

    def run(self, host: str, port: int):
        import uvicorn
        print(f"SocketServer is running on {host}:{port}")
        uvicorn.run(self.__app, host=host, port=port, log_level="info")