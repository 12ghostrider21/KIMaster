import threading
from fastapi import FastAPI
from starlette.websockets import WebSocket
from SocketServer import Server


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


class FastAPIServer:
    def __init__(self, server_instance):
        self.server: Server = server_instance
        self.app = FastAPI()
        self.manager = ConnectionManager()

        @self.app.get("/")
        def read_root():
            return {"Hello": "World"}

        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await self.manager.connect(websocket)
            print(self.manager.active_connections)
            while True:
                data = await websocket.receive_text()
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
