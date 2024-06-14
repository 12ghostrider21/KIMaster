# Importing WebSocket from FastAPI for handling websocket connections
from fastapi import WebSocket

# Importing game difficulty enumeration
from Tools.Game_Config.difficulty import EDifficulty

# Importing game mode enumeration
from Tools.Game_Config.mode import EGameMode


# Lobby class to manage clients and their roles within a game lobby
class Lobby:
    """
    A class to manage a game lobby, handling clients and their roles within the lobby.

    Attributes:
        key (str): Unique identifier for the lobby.
        p1 (WebSocket | None): WebSocket connection for player 1.
        p2 (WebSocket | None): WebSocket connection for player 2.
        difficulty (EDifficulty): Game difficulty setting.
        mode (EGameMode): Game mode setting.
        game (str): Placeholder for the game identifier.
        game_client (WebSocket | None): WebSocket connection for the game client.
        spectator_list (list[WebSocket]): List of WebSocket connections for spectators.
    """

    # Initialize the lobby with a unique key and setup empty slots for players and spectators
    def __init__(self, key: str):
        """
        Initialize the lobby with a unique key and setup empty slots for players and spectators.

        Args:
            key (str): Unique identifier for the lobby.
        """
        # Unique identifier for the lobby
        self.key: str = key
        # WebSocket connection for player 1
        self.p1: WebSocket | None = None
        # WebSocket connection for player 2
        self.p2: WebSocket | None = None
        # Game difficulty setting, default is 'easy'
        self.difficulty: EDifficulty = EDifficulty.easy
        # Game mode setting, default is 'player vs AI'
        self.mode: EGameMode = EGameMode.player_vs_ai
        # Placeholder for the game identifier
        self.game: str = ""
        # WebSocket connection for the game client
        self.game_client: WebSocket | None = None
        # List of WebSocket connections for spectators
        self.spectator_list: list[WebSocket] = []

    # Check if the lobby is empty (no players or spectators)
    def is_empty(self) -> bool:
        """
        Check if the lobby is empty (no players or spectators).

        Returns:
            bool: True if there are no players and no spectators, False otherwise.
        """
        return self.p1 is None and self.p2 is None and len(self.spectator_list) == 0

    # Get the WebSocket connection(s) based on the specified position (player 1, player 2, or spectators)
    def get(self, pos: str | None) -> WebSocket | list[WebSocket]:
        """
        Get the WebSocket connection(s) based on the specified position (player 1, player 2, or spectators).

        Args:
            pos (str | None): Position to get the WebSocket connection(s) for ("p1", "p2", "sp" for spectators, or None for all).

        Returns:
            WebSocket | list[WebSocket]: The WebSocket connection(s) based on the specified position.
        """
        if pos is None:
            return [*self.spectator_list, self.p1, self.p2]
        return {"p1": self.p1, "p2": self.p2, "sp": self.spectator_list}.get(pos)

    # Check if a given client is already in the lobby
    def in_lobby(self, client: WebSocket) -> bool:
        """
        Check if a given client is already in the lobby.

        Args:
            client (WebSocket): The WebSocket connection to check.

        Returns:
            bool: True if the client is in the lobby, False otherwise.
        """
        return client == self.p1 or client == self.p2 or client in self.spectator_list

    # Add a client to the lobby in the specified position (player 1, player 2, or spectator)
    def join(self, client: WebSocket, pos: str | None) -> bool:
        """
        Add a client to the lobby in the specified position (player 1, player 2, or spectator).

        Args:
            client (WebSocket): The WebSocket connection to add.
            pos (str | None): The position to join ("p1", "p2", or "sp" for spectators).

        Returns:
            bool: True if the client successfully joins, False otherwise.
        """
        if self.in_lobby(client):
            return False
        match pos:
            case "p1":
                if self.p1 is None:
                    self.p1 = client
                    return True
            case "p2":
                if self.p2 is None:
                    self.p2 = client
                    return True
            case "sp":
                self.spectator_list.append(client)
                return True
            case _:
                if self.p1 is None:
                    self.p1 = client
                    return True
                self.spectator_list.append(client)
                return True
        return False

    # Remove a client from the lobby
    def leave(self, client: WebSocket) -> bool:
        """
        Remove a client from the lobby.

        Args:
            client (WebSocket): The WebSocket connection to remove.

        Returns:
            bool: True if the client was successfully removed, False otherwise.
        """
        if client == self.p1:
            self.p1 = None
            return True
        if client == self.p2:
            self.p2 = None
            return True
        try:
            self.spectator_list.remove(client)
            return True
        except ValueError:
            return False

    # Swap the client's role to player 1 if the slot is available
    def swap_to_p1(self, client: WebSocket) -> bool:
        """
        Swap the client's role to player 1 if the slot is available.

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

    # Swap the client's role to player 2 if the slot is available
    def swap_to_p2(self, client: WebSocket) -> bool:
        """
        Swap the client's role to player 2 if the slot is available.

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

    # Swap the client's role to spectator
    def swap_to_spectator(self, client: WebSocket) -> bool:
        """
        Swap the client's role to spectator.

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
        return client in self.spectator_list

    # Return the current status of the lobby
    def status(self) -> dict:
        """
        Return the current status of the lobby.

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
