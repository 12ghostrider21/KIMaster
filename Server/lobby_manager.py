import threading
from hashlib import sha256
from datetime import datetime, timezone
from starlette.websockets import WebSocket
from dockerAPI import DockerAPI
from lobby import Lobby

__all__ = ["LobbyManager"]

# ********************************************************************************************************************
# LobbyManager class to manage multiple lobbies and client operations on them.
# ********************************************************************************************************************


class LobbyManager:
    def __init__(self):
        """
        Initialize a new LobbyManager.
        """
        self.lobbies: dict[str, Lobby] = {}
        self.docker: DockerAPI = DockerAPI()

    def _generate_lobby_key(self) -> str:
        """
        Generate a unique key for a new lobby using SHA256 hash of the current timestamp.

        :return: A unique SHA256 hash string.
        """
        time_bytes = str(datetime.now(timezone.utc).timestamp()).encode('utf-8')  # current UTC timestamp to bytes
        sha256_hash = sha256(time_bytes).hexdigest()  # Calculate the SHA256 hash of the timestamp bytes
        if sha256_hash in self.lobbies.keys():  # Check if the hash already exists in the lobbies dictionary
            return self._generate_lobby_key()  # Recursively generate a new lobby key if the hash already exists
        return sha256_hash  # Return the unique SHA256 hash

    def create_lobby(self) -> str:
        """
        Create a new lobby and start its game client.

        :return: The unique key of the newly created lobby.
        """
        key: str = self._generate_lobby_key()
        self.lobbies[key] = Lobby(key)
        self.docker.start_game_client(key)
        return key

    def lobby_exist(self, lobby_key: str) -> bool:
        """
        Check if a lobby with the given key exists.

        :param lobby_key: The unique key of the lobby.
        :return: True if the lobby exists, False otherwise.
        """
        return lobby_key in self.lobbies.keys()

    def remove_lobby(self, lobby_key: str) -> bool:
        """
        Remove a lobby by its key.

        :param lobby_key: The unique key of the lobby to remove.
        :return: True if the lobby was successfully removed, False otherwise.
        """
        removed = self.lobbies.pop(lobby_key, None)
        if removed is None:
            return False
        return True

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # client operation on lobbies

    def get_lobby(self, client: WebSocket | str) -> Lobby | None:
        """
        Retrieve a lobby by its key or a client's WebSocket.

        :param client: The lobby key or WebSocket client.
        :return: The corresponding Lobby object or None if not found.
        """
        if isinstance(client, str):
            return self.lobbies.get(client, None)
        for key, lobby in self.lobbies.items():
            if lobby.in_lobby(client):
                return lobby
            if lobby.game_client == client:
                return lobby
        return None

    def leave_lobby(self, client: WebSocket) -> bool:
        """
        Remove a client from their current lobby.

        :param client: The WebSocket client to remove.
        :return: True if the client successfully left, False otherwise.
        """
        lobby: Lobby = self.get_lobby(client)
        if lobby is None:
            return False  # client not in a lobby to leave
        if not lobby.leave(client):
            return False  # error on leave
        if lobby.is_empty():  # delete game_client on empty lobby
            threading.Thread(target=self.__delete_task, args=[lobby.key]).start()  # leave without waiting on delete
        return True  # successfully left

    def __delete_task(self, lobby_key):
        self.remove_lobby(lobby_key)
        self.docker.stop_game_client(lobby_key)

    def join_lobby(self, lobby_key: str, client: WebSocket, pos: str) -> bool:
        """
        Add a client to a lobby with a specified role.

        :param lobby_key: The unique key of the lobby to join.
        :param client: The WebSocket client to add.
        :param pos: The role/position to join as ('p1', 'p2', 'sp', or None).
        :return: True if the client successfully joined, False otherwise.
        """
        if not self.lobby_exist(lobby_key):
            return False  # lobby does not exist
        return self.lobbies.get(lobby_key).join(client, pos)

    def swap_to(self, pos: str, client: WebSocket) -> bool:
        """
        Swap a client's position in their current lobby.

        :param pos: The role/position to swap to ('p1', 'p2', 'sp').
        :param client: The WebSocket client to swap.
        :return: True if the swap was successful, False otherwise.
        """
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
        """
        Get the status of a specific lobby.

        :param lobby_key: The unique key of the lobby.
        :return: A dictionary with the lobby status or None if the lobby does not exist.
        """
        lobby: Lobby = self.lobbies.get(lobby_key)
        return lobby.status() if lobby else None

    def get_pos_of_client(self, client: WebSocket) -> str | None:
        """
        Get the position of a client in their current lobby.

        :param client: The WebSocket client.
        :return: The position string ('p1', 'p2', 'sp') or None if the client is not in a lobby.
        """
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
        """
        Connect a game client to a lobby.

        :param lobby_key: The unique key of the lobby.
        :param game_client: The WebSocket of the game client.
        :return: True if the game client was successfully connected, False otherwise.
        """
        lobby: Lobby = self.get_lobby(lobby_key)
        if lobby is None:
            return False  # key does not exist
        lobby.game_client = game_client
        return True  # game client connected with lobby

    def disconnect_game_client(self, game_client: WebSocket) -> bool:
        """
        Disconnect a game client from its current lobby.

        :param game_client: The WebSocket of the game client.
        :return: True if the game client was successfully disconnected, False otherwise.
        """
        lobby: Lobby = self.get_lobby(game_client)
        if lobby is None:
            return False  # game client not in a lobby
        lobby.game_client = None
        return True  # game client removed from lobby
