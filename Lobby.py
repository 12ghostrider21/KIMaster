from starlette.websockets import WebSocket


class Lobby:
    def __init__(self, key: str):
        self.p1 = None
        self.p2 = None
        self.spectator_list: list = []
        self.key: str = key
        self.game_client = None

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
