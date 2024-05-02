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

        @self.app.get("/connections")
        def read_connections():
            return self.manager.active_connections.__str__()

        @self.app.post("/join/{lobbykey}")
        def post_join(lobbykey):
            self.server.toServer(data=lobbykey)

        @self.app.get("/clients")
        def read_clients():
            with self.server.lock:
                return {"clients": list(self.server.clients.keys())}

        @self.app.post("/toServer")
        def msg(data: dict):
            return self.server.toServer(data=data)

        @self.app.post("/send_message_to_client/{client_id}")
        def send_message_to_client(client_id: int, message: str):
            with self.server.lock:
                if client_id in self.server.clients:
                    client_socket = self.server.clients[client_id]
                    try:
                        self.server.send(client_socket, message)
                        response = client_socket.recv(1024).decode()  # Beispiel für eine Rückmeldung vom Client
                        return {"status": "success", "response": response}
                    except Exception as e:
                        return {"status": "error", "message": str(e)}
                else:
                    return {"status": "error", "message": f"Client with ID {client_id} not found"}

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
