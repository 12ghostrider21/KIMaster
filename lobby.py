import datetime
import hashlib
from starlette.websockets import WebSocket

class Lobby:
    def __init__(self, key: str):
        self._p1: WebSocket | None = None
        self._p2: WebSocket | None = None
        self._spectator_list: list[WebSocket] = []
        self.key: str = key
        self.game_client: WebSocket | None = None

    def start(self) -> bool:
        # add start requirements
        return False

    def empty(self) -> bool:
        return self._p1 is None and self._p2 is None and len(self._spectator_list) == 0

    def client_in_lobby(self, client: WebSocket) -> bool:
        if client == self._p1 or client == self._p2:
            return True
        return client in self._spectator_list

    def join(self, client: WebSocket) -> bool:
        if self.client_in_lobby(client):
            print(f"Client is already in lobby {self.key}.")
            return False

        if self._p1 is None:
            self._p1 = client
            print(f"Player 1 joined successfully lobby {self.key}.")
            return True
        if self._p2 is None:
            self._p2 = client
            print(f"Player 2 joined successfully lobby {self.key}.")
            return True
        self._spectator_list.append(client)
        print(f"Client joined as a spectator in lobby {self.key}.")
        return True

    def leave(self, client: WebSocket) -> bool:
        if not self.client_in_lobby(client):
            print(f"Client {client} not in Lobby {self.key}")
            return False

        if client == self._p1:
            self._p1 = None
            print(f"Player 1 left lobby {self.key}")
            return True
        if client == self._p2:
            self._p2 = None
            print(f"Player 2 left lobby {self.key}")
            return True
        self._spectator_list.remove(client)
        print(f"Spectator {client} left lobby {self.key}")
        return True

    def swap_to_p1(self, client: WebSocket) -> bool:
        if self._p1 is None:
            self._p1 = client
            if client == self._p2:
                self._p2 = None
                return True
            if client in self._spectator_list:
                self._spectator_list.remove(client)
            return True
        return False

    def swap_to_p2(self, client: WebSocket) -> bool:
        if self._p2 is None:
            self._p2 = client
            if client == self._p1:
                self._p1 = None
                return True
            if client in self._spectator_list:
                self._spectator_list.remove(client)
            return True
        return False

    def swap_to_spectator(self, client: WebSocket) -> bool:
        if client == self._p1:
            self._spectator_list.append(client)
            self._p1 = None
            return True
        if client == self._p2:
            self._spectator_list.append(client)
            self._p2 = None
            return True
        return False

    def __dict__(self) -> dict:
        p1_status = "True" if self._p1 else "False"
        p2_status = "True" if self._p2 else "False"
        spectator_count = len(self._spectator_list)
        game = "True" if self.game_client else "False"
        return {"P1": p1_status, "P2": p2_status, "Spectators": spectator_count, "GameClient": game, "key": self.key}

    def __str__(self):
        return f"{self.__dict__()}"

    @property
    def p1(self):
        return self._p1

    @property
    def p2(self):
        return self._p2

    @property
    def spectator_list(self):
        return self._spectator_list


class LobbyManager:
    def __init__(self):
        self.lobbies: dict[str, Lobby] = {}

    def _generate_lobby_key(self) -> str:
        current_time = datetime.datetime.now(datetime.timezone.utc).timestamp()
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

    def remove_lobby(self, lobby_key: str) -> bool:
        removed = self.lobbies.pop(lobby_key, None)
        return removed is not None

    def lobby_exist(self, lobby_key: str) -> bool:
        return lobby_key in self.lobbies.keys()

    # ***************************************************************************
    # clients
    def client_in_lobby(self, client: WebSocket) -> bool:
        for lobby in self.lobbies.values():
            if lobby.client_in_lobby(client):
                return True
        return False

    def join(self, key: str, client: WebSocket) -> bool:
        if self.lobby_exist(lobby_key=key):
            return self.lobbies.get(key).join(client)
        print(f"Lobby '{key}' does not exist!")
        return False

    def leave(self, client: WebSocket) -> bool:
        lobby: Lobby = self.lobby_of_client(client)
        if lobby:
            if lobby.leave(client):
                if lobby.empty():
                    self.remove_lobby(lobby.key)
                return True
        return False  # not in a lobby

    def lobby_of_client(self, client: WebSocket) -> Lobby | None:
        for key, lobby in self.lobbies.items():
            if lobby.client_in_lobby(client):
                return lobby
        return None

    def swap_to(self, pos: str, client: WebSocket):
        lobby: Lobby = self.lobby_of_client(client)
        if lobby:
            match pos:
                case "p1":
                    return lobby.swap_to_p1(client)
                case "p2":
                    return lobby.swap_to_p2(client)
                case "sp":
                    return lobby.swap_to_spectator(client)
                case _:
                    return False
        print("Swap failed! Client not in Lobby!")
        return False  # not in a lobby

    def lobby_status(self, key: str) -> dict | None:
        lobby: Lobby = self.lobbies.get(key)
        return lobby.__dict__() if lobby else None

    def get_pos_of_client(self, client: WebSocket) -> str | None:
        lobby: Lobby = self.lobby_of_client(client)
        if lobby:
            if lobby.p1 == client:
                return "p1"
            if lobby.p2 == client:
                return "p2"
            if client in lobby.spectator_list:
                return "sp"
        return None  # client not in a lobby

    # ***************************************************************************
    # GameClients

    def lobby_of_game_client(self, game_client: WebSocket) -> Lobby | None:
        for lobby in self.lobbies.values():
            if lobby.game_client == game_client:
                return lobby
        return None

    def connect_game_client(self, lobby_key: str, game_client: WebSocket):
        lobby: Lobby = self.lobbies.get(lobby_key)
        if lobby:
            if lobby.game_client is None:
                lobby.game_client = game_client
                return True
        return False

    def disconnect_game_client(self, client: WebSocket) -> bool:
        lobby: Lobby = self.lobby_of_game_client(client)
        if lobby:
            if lobby.game_client:
                lobby.game_client = None
                return True
        return False
