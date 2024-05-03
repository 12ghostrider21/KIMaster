import datetime
import os
import random
import threading

from code.backend.api.FrontendManager import F_Manager
from code.backend.api.SocketServer import Server
from fastapi import FastAPI
from starlette.websockets import WebSocket
from code.backend.api.Lobby import Lobby
from code.backend.api.GameClient import GameClient


class FastAPIServer:
    def __init__(self, server_instance):
        self.server: Server = server_instance
        self.app = FastAPI()
        self.manager: F_Manager = F_Manager()
        self.lobbies = {}

        @self.app.get("/")
        def read_root():
            return {"Hello": "World"}

        @self.app.post("/create/lobby")
        def create_lobby():
            return random.randint(0, 100).__str__().encode()

        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await self.manager.connect(websocket)
            print(self.manager.active_connections)
            while True:
                data = await websocket.receive_text()

                if data.get("create"):
                    key = str(hash(datetime.datetime.now()))
                    self.lobbies[key] = Lobby()
                    print(f"{key=}")
                    self.server.toServer(key)
                    await websocket.send_json({"key": key, "msg": "Lobby created successfully."})

                print(data)
                await websocket.send_text(data)
                if data == "exit":
                    break
            await websocket.close()
            self.manager.disconnect(websocket)

    def run(self, host='127.0.0.1', port=8000):
        threading.Thread(target=self.server.start, daemon=True).start()
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)


if __name__ == "__main__":
    server = Server()
    api = FastAPIServer(server)
    api.run()
