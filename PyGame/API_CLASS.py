import uvicorn
from fastapi import FastAPI
from TicTacToeGame import TicTacToeGame
from Lobby import Lobby

class API(FastAPI):
    def __init__(self):
        super().__init__()
        self.lobbyliste: dict[str, Lobby] = {}

        @self.get("/")
        async def index():
            return "Hello World"

        @self.post("/newgame")
        async def newGame(gameid: int, token):
            if token in self.LOBBYLIST:
                self.LOBBYLIST[token] = TicTacToeGame()

        @self.post("/test")
        async def test(data):
            print(data)


if __name__ == "__main__":
    uvicorn.run(API(), host="127.0.0.1", port=8000)
