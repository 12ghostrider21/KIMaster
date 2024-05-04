from starlette.websockets import WebSocket
from Games.IGame import IGame
from Game.GameClient import GameClient
from pygame import surface


class Lobby:
    def __init__(self, key: str):
        self.p1 = None
        self.p2 = None
        self.spectator_list: list = []
        self.key: str = key
        self.game: IGame | None = None
        self.game_client: GameClient | None = None

    def client_in_lobby(self, client: WebSocket) -> bool:
        if client == self.p1:
            return True
        if client == self.p2:
            return True
        return client in self.spectator_list

    def join(self, client: WebSocket):
        if self.client_in_lobby(client):
            return "Client is already in lobby."
        if self.p1 is None:
            self.p1 = client
            return "Player 1 joined successfully."
        elif self.p2 is None:
            self.p2 = client
            return "Player 2 joined successfully."
        else:
            if client in self.spectator_list:
                return "Client is already a spectator."
            self.spectator_list.append(client)
            return "Client joined as a spectator."

    def leave(self, client: WebSocket):
        if self.client_in_lobby(client):
            if client == self.p1:
                self.p1 = None
                return "Player 1 leaved"
            if client == self.p2:
                self.p2 = None
                return "Player 2 leaved"
            self.spectator_list.remove(client)
            return f"Spectator {client=} leaved"
        return "Client not in Lobby"

    def get_board_images(self, board: surface, valid_moves=False, from_pos=0, *args: any):
        png_p1 = self.game.draw(board, 1, valid_moves, from_pos, args)
        png_p2 = self.game.draw(board, -1, valid_moves, from_pos, args)
        return png_p1, png_p2

    def __str__(self) -> str:
        players = f"Players: {self.p1} vs {self.p2}" if self.p1 and self.p2 else "Players: None"
        spectators = f"Spectators: {', '.join(self.spectator_list)}" if self.spectator_list else "Spectators: None"
        game_state = f"Game: {self.game}" if self.game else "Game: None"
        return f"Lobby Key: {self.key}\n{players}\n{spectators}\n{game_state}"
