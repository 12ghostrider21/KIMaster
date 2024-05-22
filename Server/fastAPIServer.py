import json
import threading
import uvicorn

from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketDisconnect, WebSocketState

from lobby import Lobby
from e_response import EResponse
from socketServer import SocketServer

from dockerAPI import DockerAPI


class FastAPIServer:
    def __init__(self):
        self.__app = FastAPI()
        self.socket_server: SocketServer = SocketServer()
        self.active_connections: list[WebSocket] = []
        self.docker_api: DockerAPI = DockerAPI() 

        @self.__app.websocket("/ws")
        async def websocket_endpoint(client: WebSocket):
            await self.connect(client)
            while True:
                try:
                    readObject: dict = await client.receive_json()
                except json.decoder.JSONDecodeError:
                    await self.send_response(client, EResponse.ERROR, "Received data is not a correct json!")
                    continue
                except WebSocketDisconnect:
                    break
                # command handling
                command: str = readObject.get("command")
                match command:
                    case "exit":
                        break
                    case "play":
                        await self.handle_play_command(client, readObject)
                    case "debug":
                        await self.handle_debug_command(client, readObject)
                    case "lobby":
                        await self.handle_lobby_command(client, readObject)
                    case _:
                        await self.send_response(client, EResponse.ERROR, f"Command: '{command}' not found!")
            await self.disconnect(client)

    # *************************************************************************************************************
    # handling
    async def handle_debug_command(self, client: WebSocket, read_object: dict) -> None:
        lobby_key: str = read_object.get("key")
        command_key: str = read_object.get("command_key")
        match command_key:
            case "list_lobby":
                print(self.socket_server.lobby_manager.lobbies)

    async def handle_lobby_command(self, client: WebSocket, read_object: dict) -> None:
        lobby_key: str = read_object.get("key")
        command_key: str = read_object.get("command_key")
        match command_key:
            case "create":
                if not self.socket_server.lobby_manager.client_in_lobby(client):
                    lobby_key: str = self.socket_server.lobby_manager.create_lobby()
                    self.socket_server.lobby_manager.join(lobby_key, client)
                    self.docker_api.startGameClient(lobby_key)
                    await self.send_response(client, EResponse.SUCCESS, "Lobby created!", {"key": lobby_key})
                else:
                    await self.send_response(client, EResponse.ERROR, "Client already in a lobby!")
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "join":
                if not self.socket_server.lobby_manager.lobby_exist(lobby_key):
                    await self.send_response(client, EResponse.ERROR, f"Lobby does not exist!",{"key": lobby_key})
                    return
                if self.socket_server.lobby_manager.client_in_lobby(client):
                    await self.send_response(client, EResponse.ERROR, "Client already in a lobby!")
                    return
                if not self.socket_server.lobby_manager.join(lobby_key, client):
                    await self.send_response(client, EResponse.ERROR, f"Failed to join lobby!", {"key": lobby_key})
                    return
                await self.send_response(client, EResponse.SUCCESS, f"Joined lobby!", {"key": lobby_key})
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "leave":
                lobby: Lobby = self.socket_server.lobby_manager.lobby_of_client(client)
                if not self.socket_server.lobby_manager.leave(client):
                    await self.send_response(client, EResponse.ERROR, f"Client not in a lobby!")
                    return
                await self.send_response(client, EResponse.SUCCESS, f"Client left lobby!")
                if lobby:
                    if lobby.empty():
                        self.docker_api.stopGameClient(lobby.key)
                        self.docker_api.removeGameClient(lobby.key)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "swap":
                pos: str = read_object.get("pos")
                lobby: Lobby = self.socket_server.lobby_manager.lobby_of_client(client)
                if lobby is None:
                    await self.send_response(client, EResponse.ERROR, "Client not in a lobby!")
                    return
                if pos not in ["p1", "p2", "sp"]:
                    await self.send_response(client, EResponse.ERROR, f"Pos unknown!", {"pos": pos})
                    return
                if not self.socket_server.lobby_manager.swap_to(pos, client):
                    await self.send_response(client, EResponse.ERROR, f"Pos already occupied!", {"pos": pos})
                    return
                await self.send_response(client, EResponse.SUCCESS, f"Client swapped!", {"pos": pos})
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "pos":
                pos = self.socket_server.lobby_manager.get_pos_of_client(client)
                if pos is None:
                    await self.send_response(client, EResponse.ERROR, "Client not in a lobby!")
                    return
                await self.send_response(client, EResponse.SUCCESS, f"Client pos is: '{pos}'!")
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "status":
                status: dict = self.socket_server.lobby_manager.lobby_status(lobby_key)
                if status is None:
                    await self.send_response(client, EResponse.ERROR, f"Lobby:'{lobby_key}' not found!")
                    return
                await self.send_response(client, EResponse.SUCCESS, f"Status of lobby: '{lobby_key}'", status)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case _:
                await self.send_response(client, EResponse.ERROR, f"Command '{command_key}' not found!")

    # *************************************************************************************************************

    async def handle_play_command(self, client: WebSocket, read_object: dict) -> None:
        command_key: str = read_object.get("command_key")
        lobby = self.socket_server.lobby_manager.lobby_of_client(client)
        if lobby is None:
            await self.send_response(client, EResponse.ERROR, "Client not in a lobby!")
            return
        game_client = lobby.game_client
        if game_client is None:
            await self.send_response(client, EResponse.ERROR, "No Game client connected! Try later again.")
            return
        pos = self.socket_server.lobby_manager.get_pos_of_client(client)
        if pos is None:
            await self.send_response(client, EResponse.ERROR, "'pos' entry not set!", {"pos": pos})
            return
        if pos == "sp":  # check if command is from a spectator!
            await self.send_response(client, EResponse.ERROR, "A spectator can not play!")
            return
        # mask data from read_object

        data = {"player_pos": pos, "key": lobby.key}
        data.update(read_object)

        match command_key:
            case "create":
                # game, mode, difficulty
                await self.socket_server.send_cmd(game_client, "play", "create", data)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "valid_moves":
                # [pos]
                await self.socket_server.send_cmd(game_client, "play", "valid_moves", data)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "make_move":
                # move
                await self.socket_server.send_cmd(game_client, "play", "make_move", data)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "undo_move":
                # num
                await self.socket_server.send_cmd(game_client, "play", "undo_move", data)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "surrender":
                await self.socket_server.send_cmd(game_client, "play", "surrender", data)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "quit":
                await self.socket_server.send_cmd(game_client, "play", "quit", data)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "new_game":
                await self.socket_server.send_cmd(game_client, "play", "new_game", data)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "blunder":
                await self.socket_server.send_cmd(game_client, "play", "blunder", data)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "timeline":
                # num
                await self.socket_server.send_cmd(game_client, "play", "timeline", data)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "step":
                await self.socket_server.send_cmd(game_client, "play", "step", data)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "unstep":
                await self.socket_server.send_cmd(game_client, "play", "unstep", data)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "evaluate":
                # game, difficulty, num
                data.update({"mode": "playerai_vs_ai"})
                await self.socket_server.send_cmd(game_client, "play", "evaluate", data)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "stop_evaluate":
                await self.socket_server.send_cmd(game_client, "play", "stop_evaluate", data)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case _:
                await self.send_response(client, EResponse.ERROR, f"Command '{command_key}' not found!")

    # *************************************************************************************************************

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        print(f"FrontEnd Client connected as: {websocket}")
        self.active_connections.append(websocket)

    async def disconnect(self, client: WebSocket):
        if client.client_state == WebSocketState.CONNECTED:
            await client.close(code=1000, reason="Server initiated closure")
        lobby: Lobby = self.socket_server.lobby_manager.lobby_of_client(client)
        if lobby:
            if lobby.leave(client):  # true if in lobby
                if lobby.empty():
                    self.socket_server.lobby_manager.remove_lobby(lobby.key)
                    self.docker_api.stopGameClient(lobby.key)
                    self.docker_api.removeGameClient(lobby.key)
                    print(f"Lobby {lobby.key} removed!")
        print(f"FrontEnd Client disconnected as: {client}")
        self.active_connections.remove(client)

    async def send_cmd(self, client: WebSocket,
                       command: str, command_key: str,
                       data: dict | None = None):
        cmd = {"command": command, "command_key": command_key}
        if data is not None:
            cmd.update(data)
        await client.send_json(cmd)

    async def send_response(self, client: WebSocket,
                            response_code: EResponse,
                            response_msg: str,
                            data: dict | None = None):
        cmd = {"response_code": response_code.value, "response_msg": response_msg}
        if data is not None:
            cmd.update(data)
        await client.send_json(cmd)

    def run(self, host: str, port: int):
        print(f"FastApiServer is running on {host}:{port}")
        uvicorn.run(self.__app, host=host, port=port, log_level="info", ws_ping_timeout=None)

    def start(self, host_fast_api, port_fast_api, host_socket_server, port_socket_server):
        t0 = threading.Thread(target=self.socket_server.run, args=(host_socket_server, port_socket_server))
        t1 = threading.Thread(target=self.run, args=(host_fast_api, port_fast_api))
        t0.start(), t1.start()
