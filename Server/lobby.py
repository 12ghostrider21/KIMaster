# Importing WebSocket from FastAPI for handling websocket connections
from fastapi import WebSocket
from Tools.Game_Config.difficulty import EDifficulty
from Tools.Game_Config.mode import EGameMode


# Lobby class to manage clients and their roles within a game lobby
class Lobby:
    # Initialize the lobby with a unique key and setup empty slots for players and spectators
    def __init__(self, key: str):
        # Unique identifier for the lobby
        self.key: str = key
        # WebSocket connection for player 1
        self.p1: WebSocket | None = None
        # WebSocket connection for player 2
        self.p2: WebSocket | None = None
        # Game difficulty setting, default is 'easy'
        self.difficulty: EDifficulty = EDifficulty.easy
        # Game mode setting, default is 'player vs AI'
        self.mode: EGameMode = EGameMode.player_vs_kim
        # Placeholder for the game identifier
        self.game: str = ""
        # WebSocket connection for the game client
        self.game_client: WebSocket | None = None
        # List of WebSocket connections for spectators
        self.spectator_list: list[WebSocket] = []
        self.game_running: bool = False

    # Check if the lobby is empty (no players or spectators)
    def is_empty(self) -> bool:
        return self.p1 is None and self.p2 is None and len(self.spectator_list) == 0

    # Get the WebSocket connection(s) based on the specified position (player 1, player 2, or spectators)
    def get(self, pos: str | None) -> WebSocket | list[WebSocket]:
        if pos is None:
            return [*self.spectator_list, self.p1, self.p2]
        return {"p1": self.p1, "p2": self.p2, "sp": self.spectator_list}.get(pos)

    # Check if a given client is already in the lobby
    def in_lobby(self, client: WebSocket) -> bool:
        return client == self.p1 or client == self.p2 or client in self.spectator_list

    # Add a client to the lobby in the specified position (player 1, player 2, or spectator)
    def join(self, client: WebSocket, pos: str | None) -> bool:
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
        if client == self.p1:
            if self.game_running:
                return False
            self.p1 = None
            return True
        if client == self.p2:
            if self.game_running:
                return False
            self.p2 = None
            return True
        try:
            self.spectator_list.remove(client)
            return True
        except ValueError:
            return False

    # Swap the client's role to player 1 if the slot is available
    def swap_to_p1(self, client: WebSocket) -> bool:
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
        return {
            "P1": self.p1 is not None,
            "P2": self.p2 is not None,
            "Spectators": len(self.spectator_list),
            "GameClient": self.game_client is not None,
            "GameRunning": self.game_running,
            "key": self.key
        }
