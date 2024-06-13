import numpy as np
from fastapi import WebSocket

from Tools.Game_Config.difficulty import EDifficulty
from Tools.Game_Config.mode import EGameMode


# ********************************************************************************************************************
# Lobby class to manage a single lobby's clients and their roles (player 1, player 2, spectators).
# ********************************************************************************************************************

class Lobby:
    """
    A class to represent a game lobby, managing clients and their roles (player 1, player 2, spectators).

    Attributes:
        key (str): Unique identifier for the lobby.
        p1 (WebSocket | None): WebSocket connection for player 1.
        p2 (WebSocket | None): WebSocket connection for player 2.
        game_client (WebSocket | None): WebSocket connection for the game client.
        spectator_list (list[WebSocket]): List of WebSocket connections for spectators.
    """

    def __init__(self, key: str):
        """
        Initializes the Lobby with a unique key and empty slots for players and spectators.

        Args:
            key (str): Unique identifier for the lobby.
        """
        self.key: str = key
        self.p1: WebSocket | None = None
        self.p2: WebSocket | None = None
        self.difficulty: EDifficulty = EDifficulty.easy
        self.mode: EGameMode = EGameMode.player_vs_ai
        self.game: str = ""
        self.game_client: WebSocket | None = None
        self.spectator_list: list[WebSocket] = []

    def is_empty(self) -> bool:
        """
        Checks if the lobby is empty.

        Returns:
            bool: True if there are no players and no spectators, False otherwise.
        """
        return self.p1 is None and self.p2 is None and len(self.spectator_list) == 0

    def get(self, pos: str | None) -> WebSocket | list[WebSocket]:
        if pos is None:
            return [*self.spectator_list, self.p1, self.p2]
        return {"p1": self.p1, "p2": self.p2, "sp": self.spectator_list}.get(pos)

    def in_lobby(self, client: WebSocket) -> bool:
        """
        Checks if a given client is already in the lobby.

        Args:
            client (WebSocket): The WebSocket connection to check.

        Returns:
            bool: True if the client is in the lobby, False otherwise.
        """
        return client == self.p1 or client == self.p2 or client in self.spectator_list

    def join(self, client: WebSocket, pos: str | None) -> bool:
        """
        Adds a client to the lobby in the specified position.

        Args:
            client (WebSocket): The WebSocket connection to add.
            pos (str | None): The position to join ("p1", "p2", or "sp" for spectators).

        Returns:
            bool: True if the client successfully joins, False otherwise.
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
        Removes a client from the lobby.

        Args:
            client (WebSocket): The WebSocket connection to remove.

        Returns:
            bool: True if the client was successfully removed, False otherwise.
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
        Swaps the client's role to player 1 if the slot is available.

        Args:
            client (WebSocket): The WebSocket connection to swap.

        Returns:
            bool: True if the swap was successful, False otherwise.
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
        Swaps the client's role to player 2 if the slot is available.

        Args:
            client (WebSocket): The WebSocket connection to swap.

        Returns:
            bool: True if the swap was successful, False otherwise.
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
        Swaps the client's role to spectator.

        Args:
            client (WebSocket): The WebSocket connection to swap.

        Returns:
            bool: True if the swap was successful, False otherwise.
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

    def status(self) -> dict:
        """
        Returns the current status of the lobby.

        Returns:
            dict: A dictionary containing the status of players, spectators, game client, and lobby key.
        """
        return {
            "P1": "True" if self.p1 else "False",
            "P2": "True" if self.p2 else "False",
            "Spectators": len(self.spectator_list),
            "GameClient": "True" if self.game_client else "False",
            "key": self.key
        }
