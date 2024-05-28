from starlette.websockets import WebSocket
from Tools.game_states import GAMESTATE

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
        self.state: GAMESTATE = GAMESTATE.WAITING
        self.game: str | None = None
        self.mode: str | None = None
        self.difficulty: str | None = None

    def ready_tp_start(self) -> bool:
        if self.mode in ["player_vs_player", "playerai_vs_playerai"]:
            return self.p1 is not None and self.p2 is not None
        if self.mode in ["player_vs_ai", "playerai_vs_ai"]:
            return self.p1 is not None and self.p2 is None
        raise TypeError("Mode is not available", self.mode)

    def get_client(self, pos: str) -> WebSocket | list[WebSocket]:
        return {"p1": self.p1, "p2": self.p2, "sp": self.spectator_list}.get(pos)

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
                "GameState": self.state.name,
                "key": self.key}

    def __str__(self):
        return self.status().__str__()
