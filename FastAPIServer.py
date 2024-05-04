import json
import threading
from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketState, WebSocketDisconnect
from SocketServer import SocketServer


class FastAPIServer:
    def __init__(self):
        self.__app = FastAPI()
        self.socket_server: SocketServer = SocketServer()
        self.active_connections: list[WebSocket] = []

        @self.__app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await self.connect(websocket)
            while True:
                try:
                    readObject: dict = await websocket.receive_json()
                except json.decoder.JSONDecodeError:
                    await self.send_message("Received data is not a correct json!", websocket)
                    continue
                except WebSocketDisconnect:
                    break

                command: str | None = readObject.get("command")
                command_key = readObject.get("command_key")
                match command:
                    case "exit":
                        break
                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    case "lobby":
                        match command_key:
                            case "create":
                                msg, key = self.socket_server.new_lobby(websocket)
                                if key is None:  # if user in lobby, cant create a new lobby!
                                    await self.send_message(msg, websocket)
                                    continue
                                result = self.socket_server.join_lobby(key, websocket)
                                await self.send_message(f"{result}, {key}", websocket)

                            # *********************************************************************************

                            case "load":
                                key = readObject.get("key")
                                game_name = readObject.get("game_name")
                                if not self.socket_server.lobby_exist(key):
                                    await self.send_message(f"Lobby with {key=} does not exist!", websocket)
                                    continue
                                msg = self.socket_server.load_game(key, game_name)
                                await self.send_message(msg, websocket)

                            # *********************************************************************************

                            case "join":
                                key = readObject.get("key")
                                if not self.socket_server.lobby_exist(key):
                                    await self.send_message(f"Lobby with {key=} does not exist!", websocket)
                                    continue
                                result = self.socket_server.join_lobby(key, websocket)
                                await self.send_message(result, websocket)

                            # *********************************************************************************

                            case "leave":
                                key = readObject.get("key")
                                if not self.socket_server.lobby_exist(key):
                                    await self.send_message(f"Lobby with {key=} does not exist!", websocket)
                                    continue
                                result = self.socket_server.leave_lobby(key, websocket)
                                await self.send_message(result, websocket)
                            case _:
                                await self.send_message("Command not found!", websocket)

                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                    case _:
                        await self.send_message("Command not found!", websocket)
            await self.disconnect(websocket)

    def start(self, host_FastAPI, port_FastAPI, host_SocketServer, port_SocketServer):
        t0 = threading.Thread(target=self.socket_server.run, args=(host_SocketServer, port_SocketServer))
        t1 = threading.Thread(target=self.run, args=(host_FastAPI, port_FastAPI))
        t0.start(), t1.start()

    # *************************************************************************************************************

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        print(f"FrontEnd Client connected with: {websocket}")
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.close(code=1000, reason="Server initiated closure")
        print(f"FrontEnd Client disconnected with: {websocket}")
        self.active_connections.remove(websocket)
        key = self.socket_server.get_lobby_key_of_client(websocket)
        if key:
            self.socket_server.leave_lobby(key, websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_json(self, data: dict, websocket: WebSocket):
        await websocket.send_json(data)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def send_image(self, image_bytes: bytes, websocket: WebSocket):
        await websocket.send_bytes(image_bytes)

    def run(self, host: str, port: int):
        import uvicorn
        print(f"FastApiServer is running on {host}:{port}")
        uvicorn.run(self.__app, host=host, port=port, log_level="info")
