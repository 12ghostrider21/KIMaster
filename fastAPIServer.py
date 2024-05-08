import json
import subprocess
import threading
from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketState, WebSocketDisconnect
from socketServer import SocketServer


class FastAPIServer:
    def __init__(self):
        self.__app = FastAPI()
        self.socket_server: SocketServer = SocketServer()
        self.active_connections: list[WebSocket] = []

        @self.__app.websocket("/ws")
        async def websocket_endpoint(client: WebSocket):
            await self.connect(client)
            while True:
                try:
                    readObject: dict = await client.receive_json()
                except json.decoder.JSONDecodeError:
                    await self.send_message(client, "Received data is not a correct json!")
                    continue
                except WebSocketDisconnect:
                    break

                command: str = readObject.get("command")
                command_key: str = readObject.get("command_key")
                match command:
                    case "exit":
                        break
                    case "lobby":
                        lobby_key: str = readObject.get("key")
                        match command_key:
                            case "create":
                                if self.socket_server.lobby_manager.client_in_lobby(client):
                                    await self.send_message(client, "Client already in a lobby!")
                                    continue
                                lobby_key: str = self.socket_server.lobby_manager.create_lobby()

                                self.socket_server.lobby_manager.join(lobby_key, client)
                                await self.send_message(client, lobby_key)
                            case "start":
                                if not self.socket_server.lobby_manager.lobby_exist(lobby_key):
                                    await self.send_message(client, f"Lobby {lobby_key} does not exist!")
                                    continue
                                # replace with docker container
                                command = rf'start cmd /k python C:\Users\alex\PycharmProjects\Plattform-fuer-Vergleich-von-Spiele-KIs\DockerClient\StartClient.py 12345 localhost {lobby_key}'
                                subprocess.Popen(command, shell=True)


                            case "join":
                                if not self.socket_server.lobby_manager.lobby_exist(lobby_key):
                                    await self.send_message(client, f"Lobby {lobby_key} does not exist!")
                                    continue
                                if self.socket_server.lobby_manager.join(lobby_key, client):
                                    await self.send_message(client, f"Joined lobby {lobby_key}!")
                                    continue
                                key = self.socket_server.lobby_manager.find_lobby_of_client(client)
                                await self.send_message(client, f"You are already in lobby {key}!")
                            case "leave":
                                key = self.socket_server.lobby_manager.find_lobby_of_client(client)
                                if key is None:
                                    await self.send_message(client, f"You are not in a lobby!")
                                    continue
                                if self.socket_server.lobby_manager.leave(client):
                                    await self.send_message(client, f"You left lobby {key}!")
                                    continue
                                await self.send_message(client, f"Lobby {key} does not exist!")
                            case "swap":
                                pos: str = readObject.get("pos")
                                if pos is None:
                                    await self.send_message(client, f"Position: {pos} is not a lobby position!")
                                    continue
                                if self.socket_server.lobby_manager.swap_to(pos, client):
                                    await self.send_message(client, f"Swapped to {pos}!")
                                    continue
                                await self.send_message(client, f"Failed to swap to {pos}!")
                            case "pos":
                                if not self.socket_server.lobby_manager.client_in_lobby(client):
                                    await self.send_message(client, f"You are not in a lobby!")
                                    continue
                                pos = self.socket_server.lobby_manager.get_pos_of_client(client)
                                if pos is None:
                                    await self.send_message(client, f"Your lobby was not found!")
                                    continue
                                await self.send_message(client, f"Your pos is: {pos}")
                            case "list":
                                msg = self.socket_server.lobby_manager.list_lobby_player(lobby_key)
                                await self.send_message(client, msg)
                            case _:
                                await self.send_message(client, f"Command '{command}' not found!")

                    case _:
                        await self.send_message(client, f"Command '{command}' not found!")
            await self.disconnect(client)

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
        self.socket_server.lobby_manager.leave(websocket)
        self.active_connections.remove(websocket)

    async def send_message(self, websocket: WebSocket, message: str):
        await websocket.send_text(message)

    async def send_cmd(self, websocket: WebSocket, command: str, command_key: str, data: dict | None = None):
        cmd = {"command": command, "command_key": command_key}
        if data is not None:
            cmd.update(data)
        await websocket.send_json(data)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def send_image(self, image_bytes: bytes, websocket: WebSocket):
        await websocket.send_bytes(image_bytes)

    def run(self, host: str, port: int):
        import uvicorn
        print(f"FastApiServer is running on {host}:{port}")
        uvicorn.run(self.__app, host=host, port=port, log_level="info", ws_ping_timeout=None)
