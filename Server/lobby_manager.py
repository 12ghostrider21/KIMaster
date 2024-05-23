import threading
from hashlib import sha256
from datetime import datetime, timezone
from starlette.websockets import WebSocket
from dockerAPI import DockerAPI


# ********************************************************************************************************************
# Lobby class to manage a single lobby's clients and their roles (player 1, player 2, spectators).
# ********************************************************************************************************************

class Lobby:
    def __init__(self, key: str):
        """
        Initialize a new lobby with a unique key.

        :param key: Unique identifier for the lobby.
        """
        self.key: str = key
        self.p1: WebSocket | None = None
        self.p2: WebSocket | None = None
        self.spectator_list: list[WebSocket] = []
        self.game_client: WebSocket | None = None

    def is_empty(self) -> bool:
        """
        Check if the lobby is empty (no players or spectators).

        :return: True if the lobby is empty, False otherwise.
        """
        return self.p1 is None and self.p2 is None and len(self.spectator_list) == 0

    def in_lobby(self, client: WebSocket) -> bool:
        """
        Check if a client is in the lobby.

        :param client: The WebSocket client to check.
        :return: True if the client is in the lobby, False otherwise.
        """
        if client == self.p1 or client == self.p2:
            return True
        return client in self.spectator_list

    def join(self, client: WebSocket, pos: str) -> bool:
        """
        Add a client to the lobby in a specified role.

        :param client: The WebSocket client to add.
        :param pos: The role/position to join as ('p1', 'p2', 'sp', or None).
        :return: True if the client successfully joined, False otherwise.
        """
        if self.in_lobby(client):
            return False  # already in lobby
        match pos:
            case "p1":
                if self.p1 is None:
                    self.p1 = client
                    return True  # joined as player 1
            case "p2":
                if self.p2 is None:
                    self.p2 = client
                    return True  # joined as player 2
            case "sp":
                self.spectator_list.append(client)
                return True  # joined as spectator
            case _:
                if self.p1 is None:
                    self.p1 = client
                    return True  # initial join is always as player 1
                self.spectator_list.append(client)
                return True  # unspecified position defaults to spectator
        return False  # position is blocked or unknown

    def leave(self, client: WebSocket) -> bool:
        """
        Remove a client from the lobby.

        :param client: The WebSocket client to remove.
        :return: True if the client successfully left, False otherwise.
        """
        if client == self.p1:
            self.p1 = None
            return True  # left as player 1
        if client == self.p2:
            self.p2 = None
            return True  # left as player 2
        try:
            self.spectator_list.remove(client)
            return True  # left as spectator
        except ValueError:
            return False  # client not in lobby

    def swap_to_p1(self, client: WebSocket) -> bool:
        """
        Swap a client to player 1 position.

        :param client: The WebSocket client to swap.
        :return: True if the swap was successful, False otherwise.
        """
        if self.p1 is None:
            self.p1 = client
            if client == self.p2:
                self.p2 = None
                return True
            if client in self.spectator_list:
                self.spectator_list.remove(client)
            return True
        return False

    def swap_to_p2(self, client: WebSocket) -> bool:
        """
        Swap a client to player 2 position.

        :param client: The WebSocket client to swap.
        :return: True if the swap was successful, False otherwise.
        """
        if self.p2 is None:
            self.p2 = client
            if client == self.p1:
                self.p1 = None
                return True
            if client in self.spectator_list:
                self.spectator_list.remove(client)
            return True
        return False

    def swap_to_spectator(self, client: WebSocket) -> bool:
        """
        Swap a client to spectator position.

        :param client: The WebSocket client to swap.
        :return: True if the swap was successful, False otherwise.
        """
        if client == self.p1:
            self.spectator_list.append(client)
            self.p1 = None
            return True
        if client == self.p2:
            self.spectator_list.append(client)
            self.p2 = None
            return True
        return client in self.spectator_list  # from sp -> sp also true for response message

    def get_client_by_string(self, pos: str) -> WebSocket | None:
        """
        Get a client by their position string.

        :param pos: The position string ('p1', 'p2').
        :return: The corresponding WebSocket client or None if not found.
        """
        if pos == "p1":
            return self.p1
        if pos == "p2":
            return self.p2
        return None  # broadcast

    def status(self) -> dict:
        """
        Get the status of the lobby.

        :return: A dictionary containing the status of players, spectators, game client, and the lobby key.
        """
        return {"P1": "True" if self.p1 else "False",
                "P2": "True" if self.p2 else "False",
                "Spectators": len(self.spectator_list),
                "GameClient": "True" if self.game_client else "False",
                "key": self.key}

    def __str__(self):
        return self.status().__str__()


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
        self.docker.startGameClient(key)
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
        if lobby.is_empty():
            threading.Thread(target=self.__delete_task, args=[lobby.key]).start()
        return True  # successfully left

    def __delete_task(self, lobby_key):
        self.remove_lobby(lobby_key)
        self.docker.stopGameClient(lobby_key)
        self.docker.removeGameClient(lobby_key)

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
