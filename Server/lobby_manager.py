from datetime import datetime, timezone
from hashlib import sha256
from fastapi import WebSocket
from threading import Thread

from docker_api import DockerAPI
from lobby import Lobby


class LobbyManager:
    def __init__(self):
        self.lobbies: dict[str, Lobby] = {}
        self.docker: DockerAPI = DockerAPI()

    def _generate_lobby_key(self) -> str:
        time_bytes = str(datetime.now(timezone.utc).timestamp()).encode('utf-8')  # current UTC timestamp to bytes
        sha256_hash = sha256(time_bytes).hexdigest()  # Calculate the SHA256 hash of the timestamp bytes
        if sha256_hash in self.lobbies.keys():  # Check if the hash already exists in the lobbies dictionary
            return self._generate_lobby_key()  # Recursively generate a new lobby key if the hash already exists
        return sha256_hash  # Return the unique SHA256 hash

    def create_lobby(self) -> str:
        key: str = self._generate_lobby_key()
        self.lobbies[key] = Lobby(key)
        self.docker.start_game_client(key)
        return key

    def lobby_exist(self, lobby_key: str) -> bool:
        return lobby_key in self.lobbies.keys()

    def remove_lobby(self, lobby_key: str) -> bool:
        removed = self.lobbies.pop(lobby_key, None)
        if removed is None:
            return False
        return True

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # client operation on lobbies
    def get_lobby(self, client: WebSocket | str) -> Lobby | None:
        if isinstance(client, str):
            return self.lobbies.get(client, None)
        for key, lobby in self.lobbies.items():
            if lobby.in_lobby(client):
                return lobby
            if lobby.game_client == client:
                return lobby
        return None

    def leave_lobby(self, client: WebSocket) -> bool:
        lobby: Lobby = self.get_lobby(client)
        if lobby is None:
            return False  # client not in a lobby to leave
        if not lobby.leave(client):
            return False  # error on leave
        if lobby.is_empty():  # delete game_client on empty lobby
            Thread(target=self.__delete_task, args=[lobby.key]).start()  # leave without waiting on delete
        return True  # successfully left

    def __delete_task(self, lobby_key):
        self.remove_lobby(lobby_key)
        self.docker.stop_game_client(lobby_key)

    def join_lobby(self, lobby_key: str, client: WebSocket, pos: str) -> bool:
        if not self.lobby_exist(lobby_key):
            return False  # lobby does not exist
        return self.lobbies.get(lobby_key).join(client, pos)

    def swap_to(self, pos: str, client: WebSocket) -> bool:
        lobby: Lobby = self.get_lobby(client)
        if lobby is None:
            return False  # not in lobby
        match pos:
            case "p1":
                return lobby.swap_to_p1(client)
            case "p2":
                return lobby.swap_to_p2(client)
            case "sp":
                return lobby.swap_to_spectator(client)
            case _:
                return False

    def status_of_lobby(self, lobby_key: str) -> dict | None:
        lobby: Lobby = self.lobbies.get(lobby_key)
        return lobby.status() if lobby else None

    def get_pos_of_client(self, client: WebSocket) -> str | None:
        lobby: Lobby = self.get_lobby(client)
        if lobby:
            if lobby.p1 == client:
                return "p1"
            if lobby.p2 == client:
                return "p2"
            if client in lobby.spectator_list:
                return "sp"
        return None  # client not in a lobby

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # GameClients operations

    def connect_game_client(self, lobby_key: str, game_client: WebSocket) -> bool:
        lobby: Lobby = self.get_lobby(lobby_key)
        if lobby is None:
            return False  # key does not exist
        lobby.game_client = game_client
        return True  # game client connected with lobby

    def disconnect_game_client(self, game_client: WebSocket) -> bool:
        lobby: Lobby = self.get_lobby(game_client)
        if lobby is None:
            return False  # game client not in a lobby
        lobby.game_client = None
        return True  # game client removed from lobby
