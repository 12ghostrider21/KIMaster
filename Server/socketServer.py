import asyncio
import json
import uvicorn
from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketState, WebSocketDisconnect
from Tools.Response import R_CODE
from Tools.game_states import GAMESTATE
from lobby_manager import LobbyManager
from lobby import Lobby


class SocketServer:
    """
    WebSocket server class for handling real-time communication between game clients.
    """

    def __init__(self):
        """
        Initialize the SocketServer instance.
        """
        self.__app = FastAPI()
        self.lobby_manager: LobbyManager = LobbyManager()

        @self.__app.websocket("/ws")
        async def websocket_endpoint(game_client: WebSocket):
            """
            WebSocket endpoint for handling game client connections.
            """
            await self.connect(game_client)
            lobby: Lobby = self.lobby_manager.get_lobby(game_client)
            while True:
                try:
                    read_object: dict = await game_client.receive_json()
                except json.decoder.JSONDecodeError:
                    await self.send_response(game_client, R_CODE.NONVALIDJSON)
                    continue
                except WebSocketDisconnect:
                    break

                code: R_CODE = read_object.get("response_code")

                if code:
                    try:
                        read_object.pop("player_pos")  # remove internal information
                    except KeyError:
                        pass
                    client: WebSocket = lobby.get_client(read_object.get("player_pos"))
                    if isinstance(client, list) or client is None:
                        await self.send_broadcast(lobby, code, read_object)
                        continue
                    await self.send_response(client, code, read_object)
                    continue

                # Handle different commands
                command: str = read_object.get("command")
                command_key: str = read_object.get("command_key")
                lobby_key: str = read_object.get("key")
                match command:
                    case "exit":
                        break
                    case "game_client":
                        match command_key:
                            case "state":
                                for s in GAMESTATE:
                                    if s.name == read_object.get("state"):
                                        lobby.state = s
                            case "quit":
                                lobby.quit = True
                    case "img":
                        # Handle image reception and broadcasting
                        img1: bytes = await game_client.receive_bytes()
                        if command_key == "broadcast":
                            img2: bytes = await game_client.receive_bytes()
                            await self.broadcast_image(img1, img2, game_client)
                            continue
                        # Send image to a specific client
                        client = lobby.get_client_by_string(read_object.get("player_pos"))
                        await self.send_image(client, img1)
                        continue
                    case "login":
                        # Handle login command
                        lobby: Lobby = self.lobby_manager.lobbies.get(lobby_key)
                        if lobby is None:
                            await self.send_response(game_client, R_CODE.L_LOBBYNOTEXIST, {"key": lobby_key})
                            continue
                        self.lobby_manager.connect_game_client(lobby_key, game_client)
                        await self.send_response(game_client, R_CODE.L_JOINED, {"key": lobby_key})
                    case _:
                        await self.send_response(game_client, R_CODE.COMMANDNOTFOUND, {"command": command})
            await self.disconnect(game_client)

    async def connect(self, client: WebSocket):
        """
        Accept a WebSocket connection from a client.
        """
        await client.accept()

    async def send_cmd(self, game_client: WebSocket, command: str, command_key: str, data: dict = None):
        """
        Send a command to a game client.
        """
        cmd = {"command": command, "command_key": command_key}
        if data is not None:
            cmd.update(data)
        await game_client.send_json(cmd)

    async def send_broadcast(self, lobby: Lobby, code: R_CODE, data: dict = None):
        """
        Broadcast a message to all clients in a lobby.
        """
        if isinstance(code, int):  # GameClient int value -> R_Code
            for c in R_CODE:
                if c.value.code == code:
                    code = c
                    break
        if lobby.p1:
            await self.send_response(lobby.p1, code, data)
        if lobby.p2:
            await self.send_response(lobby.p2, code, data)
        for c in lobby.spectator_list:
            await self.send_response(c, code, data)

    async def send_response(self, client: WebSocket, code: R_CODE, data: dict = None):
        """
        Send a response to a client.
        """
        cmd = {"response_code": code.value.code, "response_msg": code.value.msg}
        if data is not None:
            cmd.update(data)
        if cmd.get("player_pos"):
            cmd.pop("player_pos")
        await client.send_json(cmd)

    async def broadcast_image(self, img_p1: bytes, img_p2: bytes, game_client: WebSocket) -> None:
        """
        Broadcast images to all clients in a lobby.
        """
        lobby: Lobby = self.lobby_manager.get_lobby(game_client)
        tasks = [asyncio.create_task(self.send_image(lobby.p1, img_p1)),
                 asyncio.create_task(self.send_image(lobby.p2, img_p2))]
        for sp in lobby.spectator_list:
            tasks.append(asyncio.create_task(self.send_image(sp, img_p1)))
        await asyncio.gather(*tasks)  # Send all images concurrently

    async def send_image(self, client: WebSocket, img: bytes):
        """
        Send an image to a client.
        """
        if client:  # Ignore None clients (broadcast)
            await client.send_bytes(img)

    async def disconnect(self, game_client: WebSocket):
        """
        Disconnect a game client.
        """
        if game_client.client_state == WebSocketState.CONNECTED:
            await game_client.close(code=1000, reason="Server initiated closure")
        self.lobby_manager.disconnect_game_client(game_client)
        print(f"GameClient disconnected: {game_client}")

    def run(self, host: str, port: int):
        """
        Run the WebSocket server.
        """
        print(f"SocketServer is running on {host}:{port}")
        uvicorn.run(self.__app, host=host, port=port, log_level="info", ws_ping_timeout=None)
