import datetime
import hashlib

from starlette.websockets import WebSocket


class Lobby:
    def __init__(self, key: str):
        self.p1: WebSocket | None = None
        self.p2: WebSocket | None = None
        self.spectator_list: list[WebSocket] = []
        self.key: str = key
        self.game_client = None

    def client_in_lobby(self, client: WebSocket) -> bool:
        if client == self.p1:
            return True
        if client == self.p2:
            return True
        return client in self.spectator_list

    def join(self, client: WebSocket) -> bool:
        if self.client_in_lobby(client):
            print(f"Client is already in lobby {self.key}.")
            return False
        if self.p1 is None:
            self.p1 = client
            print(f"Player 1 joined successfully lobby {self.key}.")
            return True
        elif self.p2 is None:
            self.p2 = client
            print(f"Player 2 joined successfully lobby {self.key}.")
            return True
        else:
            if client in self.spectator_list:
                print(f"Client is already a spectator in lobby {self.key}.")
                return False
            self.spectator_list.append(client)
            print(f"Client joined as a spectator in lobby {self.key}.")
            return True

    def leave(self, client: WebSocket) -> bool:
        if self.client_in_lobby(client):
            if client == self.p1:
                self.p1 = None
                print(f"Player 1 leaved lobby {self.key}")
                return True
            if client == self.p2:
                self.p2 = None
                print(f"Player 2 leaved lobby {self.key}")
                return True
            self.spectator_list.remove(client)
            print(f"Spectator {client=} leaved lobby {self.key}")
            return True
        print(f"Client {client} not in Lobby {self.key}")
        return False

    def swap_to_p1(self, client: WebSocket):
        if self.p1 is None:
            self.p1 = client
            if client == self.p2:
                self.p2 = None
                return True
            if client in self.spectator_list:
                self.spectator_list.remove(client)
            return True
        return False

    def swap_to_p2(self, client: WebSocket):
        if self.p2 is None:
            self.p2 = client
            if client == self.p1:
                self.p1 = None
                return True
            if client in self.spectator_list:
                self.spectator_list.remove(client)
            return True
        return False

    def swap_to_spectator(self, client: WebSocket):
        if client == self.p1:
            self.spectator_list.append(client)
            self.p1 = None
            return True
        if client == self.p2:
            self.spectator_list.append(client)
            self.p2 = None
            return True
        return False

    def __str__(self) -> str:
        p1_status = "True" if self.p1 else "False"
        p2_status = "True" if self.p2 else "False"
        spectator_count = len(self.spectator_list)

        return f"P1: {p1_status}, P2: {p2_status}, Spectators: {spectator_count}"


class LobbyManager:
    def __init__(self):
        self.lobbies: dict[str, Lobby] = {}

    def _generate_lobby_key(self) -> str:
        current_time = datetime.datetime.now(datetime.timezone.utc).timestamp()  # Get the current date and time as a Unix timestamp
        time_str = str(current_time)  # Convert the timestamp to a string
        time_bytes = time_str.encode('utf-8')  # Encode the string to bytes using UTF-8
        sha256_hash = hashlib.sha256(time_bytes)  # Calculate the SHA256 hash of the bytes
        hex_digest = sha256_hash.hexdigest()  # Get the hexadecimal representation of the hash as a string
        if hex_digest in self.lobbies.keys():
            return self._generate_lobby_key()
        return hex_digest

    def create_lobby(self) -> str:
        key = self._generate_lobby_key()
        lobby = Lobby(key)
        self.lobbies[key] = lobby
        print(f"Lobby {key} created.")
        return key

    # ***************************************************************************
    # clients
    def client_in_lobby(self, client: WebSocket) -> bool:
        for lobby in self.lobbies.values():
            if lobby.client_in_lobby(client):
                return True
        return False

    def lobby_exist(self, key: str) -> bool:
        return key in self.lobbies.keys()

    def join(self, key: str, client: WebSocket) -> bool:
        if not self.lobby_exist(key=key):
            print(f"Lobby {key} does not exist!")
            return False
        return self.lobbies[key].join(client)

    def leave(self, client: WebSocket) -> bool:
        lobby_key: str = self.find_lobby_of_client(client)
        if lobby_key is None:
            return False  # not in a lobby
        return self.lobbies.get(lobby_key).leave(client)

    def find_lobby_of_client(self, client: WebSocket) -> str | None:
        for key, lobby in self.lobbies.items():
            if lobby.client_in_lobby(client):
                return key
        return None

    def swap_to(self, pos: str, client: WebSocket):
        lobby_key: str = self.find_lobby_of_client(client)
        if lobby_key is None:
            return False  # not in a lobby
        lobby: Lobby = self.lobbies.get(lobby_key)
        if lobby is None:
            return False
        match pos:
            case "p1":
                return lobby.swap_to_p1(client)
            case "p2":
                return lobby.swap_to_p2(client)
            case "sp":
                return lobby.swap_to_spectator(client)
            case _:
                return False

    def list_lobby_player(self, key: str) -> str:
        lobby = self.lobbies.get(key)
        if lobby is None:
            return f"Lobby with key {key} does not Exist!"
        return lobby.__str__()

    def get_pos_of_client(self, client: WebSocket) -> str | None:
        key = self.find_lobby_of_client(client)
        if key is None:
            return None
        lobby: Lobby = self.lobbies.get(key)
        if lobby is None:
            return None
        if lobby.p1 == client:
            return "p1"
        if lobby.p2 == client:
            return "p2"
        if client in lobby.spectator_list:
            return "sp"

    # ***************************************************************************
    # GameClients

    def remove_game_client(self, client: WebSocket) -> bool:
        for lobby in self.lobbies.values():
            if lobby.game_client == client:
                lobby.game_client = None
                return True
        return False

    def game_client_join_lobby(self, key: str, client: WebSocket) -> bool:
        lobby: Lobby = self.lobbies.get(key)
        if lobby is None:
            return False
        if lobby.game_client is not None:
            return False
        lobby.game_client = client
        return True
