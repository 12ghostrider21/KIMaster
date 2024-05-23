import json
import uvicorn
from fastapi import FastAPI
from threading import Thread
from starlette.websockets import WebSocket, WebSocketDisconnect, WebSocketState

from lobby_manager import Lobby
from e_response import EResponse
from socketServer import SocketServer


class FastAPIServer:
    def __init__(self):
        """
        Initialize the FastAPI server, set up the WebSocket endpoint, and initialize necessary attributes.
        """
        self.__app = FastAPI()
        self.socket_server: SocketServer = SocketServer()
        self.connected_user: list[WebSocket] = []
        self.__mask: list[str] = ["command", "command_key", "pos", "key", "mode", "game", "difficulty", "num", "move"]

        @self.__app.websocket("/ws")
        async def websocket_endpoint(client: WebSocket):
            """
            WebSocket endpoint to handle client connections and commands.

            Args:
                client (WebSocket): The WebSocket client connection.

            Raises:
                JSONDecodeError: If the received payload is not a valid JSON.
                WebSocketDisconnect: If the WebSocket connection is disconnected.
            """
            await self.connect(client)
            while True:
                try:
                    readObject: dict = await client.receive_json()
                    if isinstance(readObject, str):
                        readObject = json.loads(readObject)
                    mask_flag = False
                    for e in readObject:
                        if e not in self.__mask:
                            await self.send_response(client, EResponse.ERROR, "Payload has an illegal key!",
                                                     {"ILLEGAL": e})
                            mask_flag = True
                            break
                    if mask_flag:
                        continue
                except json.decoder.JSONDecodeError:
                    await self.send_response(client, EResponse.ERROR, "Received payload is not a correct json!")
                    continue
                except WebSocketDisconnect:
                    break

                # Command redirecting
                command: str = readObject.get("command")
                match command:
                    case "exit":
                        break
                    case "play":
                        await self.handle_play_command(client, readObject)
                    case "lobby":
                        await self.handle_lobby_command(client, readObject)
                    case _:
                        await self.send_response(client, EResponse.ERROR,
                                                 "Command not found!",
                                                 {"command": command})
            await self.disconnect(client)

    async def connect(self, websocket: WebSocket):
        """
        Accept the WebSocket connection and add the client to the connected users list.

        Args:
            websocket (WebSocket): The WebSocket client connection.
        """
        await websocket.accept()
        self.connected_user.append(websocket)

    async def disconnect(self, client: WebSocket):
        """
        Handle disconnection of a WebSocket client.

        Args:
            client (WebSocket): The WebSocket client connection.
        """
        if client.client_state == WebSocketState.CONNECTED:
            await client.close(code=1000, reason="Server initiated closure")

        self.socket_server.lobby_manager.leave_lobby(client)
        print(f"FrontEnd Client disconnected as: {client}")
        self.connected_user.remove(client)

    async def send_response(self, client: WebSocket, response_code: EResponse, response_msg: str,
                            data: dict | None = None):
        """
        Send a response to the WebSocket client.

        Args:
            client (WebSocket): The WebSocket client connection.
            response_code (EResponse): The response code.
            response_msg (str): The response message.
            data (dict, optional): Additional data to send.
        """
        cmd = {"response_code": response_code.value, "response_msg": response_msg}
        if data is not None:
            cmd.update(data)
        await client.send_json(cmd)

    def run(self, host: str, port: int):
        """
        Run the FastAPI server.

        Args:
            host (str): The host address.
            port (int): The port number.
        """
        print(f"FastApiServer is running on {host}:{port}")
        uvicorn.run(self.__app, host=host, port=port, log_level="info", ws_ping_timeout=None)

    def start(self, host_fast_api, port_fast_api, host_socket_server, port_socket_server):
        """
        Start the FastAPI server and the Socket server on separate threads.

        Args:
            host_fast_api (str): The host address for the FastAPI server.
            port_fast_api (int): The port number for the FastAPI server.
            host_socket_server (str): The host address for the Socket server.
            port_socket_server (int): The port number for the Socket server.
        """
        t0 = Thread(target=self.socket_server.run, args=(host_socket_server, port_socket_server))
        t1 = Thread(target=self.run, args=(host_fast_api, port_fast_api))
        t0.start(), t1.start()

    # *************************************************************************************************************
    # Handling lobby commands

    async def handle_lobby_command(self, client: WebSocket, read_object: dict) -> None:
        """
        Handle lobby-related commands.

        Args:
            client (WebSocket): The WebSocket client connection.
            read_object (dict): The command and its associated data.
        """
        command_key: str = read_object.get("command_key")
        match command_key:
            case "create":
                lobby: Lobby = self.socket_server.lobby_manager.get_lobby(client)
                if lobby is not None:
                    await self.send_response(client, EResponse.ERROR,
                                             "Client already in a lobby!",
                                             {"key": lobby.key})
                else:
                    new_lobby_key: str = self.socket_server.lobby_manager.create_lobby()
                    self.socket_server.lobby_manager.join_lobby(new_lobby_key, client, "p1")
                    await self.send_response(client, EResponse.SUCCESS,
                                             "Lobby created!",
                                             {"key": new_lobby_key})
            case "join":
                if self.socket_server.lobby_manager.get_lobby(client) is not None:
                    await self.send_response(client, EResponse.ERROR, "Cannot join multiple lobbies!")
                    return
                lobby_key: str = read_object.get("key")
                pos: str = read_object.get("pos")
                if not self.socket_server.lobby_manager.lobby_exist(lobby_key=lobby_key):
                    await self.send_response(client, EResponse.ERROR,
                                             "Lobby does not exist!",
                                             {"key": lobby_key})
                    return
                if self.socket_server.lobby_manager.join_lobby(lobby_key, client, pos):
                    await self.send_response(client, EResponse.SUCCESS, "Joined lobby!",
                                             {"key": lobby_key,
                                              "pos": self.socket_server.lobby_manager.get_pos_of_client(client)})
                    return
                await self.send_response(client, EResponse.ERROR,
                                         "Failed to join lobby! Maybe blocked?",
                                         {"key": lobby_key})
            case "leave":
                if not self.socket_server.lobby_manager.leave_lobby(client):
                    await self.send_response(client, EResponse.ERROR, "Client not in a lobby!")
                    return
                await self.send_response(client, EResponse.SUCCESS, "Client left lobby!")
            case "swap":
                pos: str = read_object.get("pos")
                lobby: Lobby = self.socket_server.lobby_manager.get_lobby(client)
                if lobby is None:
                    await self.send_response(client, EResponse.ERROR, "Client not in a lobby!")
                    return
                if pos not in ["p1", "p2", "sp"]:
                    await self.send_response(client, EResponse.ERROR, "Position unknown!", {"pos": pos})
                    return
                if not self.socket_server.lobby_manager.swap_to(pos, client):
                    await self.send_response(client, EResponse.ERROR, "Position already occupied!", {"pos": pos})
                    return
                await self.send_response(client, EResponse.SUCCESS, "Client swapped!", {"pos": pos})
            case "pos":
                pos = self.socket_server.lobby_manager.get_pos_of_client(client)
                if pos is None:
                    await self.send_response(client, EResponse.ERROR, "Client not in a lobby!")
                    return
                await self.send_response(client, EResponse.SUCCESS, f"Client position is:", {"pos": pos})
            case "status":
                lobby: Lobby = self.socket_server.lobby_manager.get_lobby(client)
                if lobby is None:
                    await self.send_response(client, EResponse.ERROR, "Client not in a lobby!")
                    return
                await self.send_response(client, EResponse.SUCCESS, "Status of lobby.", lobby.status())
            case _:
                await self.send_response(client, EResponse.ERROR, f"Command '{command_key}' not found!")

    # *************************************************************************************************************
    # Handling play commands

    async def handle_play_command(self, client: WebSocket, read_object: dict) -> None:
        """
        Handle play-related commands.

        Args:
            client (WebSocket): The WebSocket client connection.
            read_object (dict): The command and its associated data.
        """
        command_key: str = read_object.get("command_key")
        lobby = self.socket_server.lobby_manager.get_lobby(client)
        if lobby is None:
            await self.send_response(client, EResponse.ERROR, "Client not in a lobby!")
            return
        game_client: WebSocket = lobby.game_client
        if game_client is None:
            await self.send_response(client, EResponse.ERROR, "No Game client connected! Try later again.")
            return
        pos = self.socket_server.lobby_manager.get_pos_of_client(client)
        if pos == "sp":
            await self.send_response(client, EResponse.ERROR, "A spectator cannot play!")
            return

        data = {"player_pos": pos, "key": lobby.key}
        data.update(read_object)

        match command_key:
            case "create":
                await self.socket_server.send_cmd(game_client, "play", "create", data)
            case "valid_moves":
                await self.socket_server.send_cmd(game_client, "play", "valid_moves", data)
            case "make_move":
                await self.socket_server.send_cmd(game_client, "play", "make_move", data)
            case "undo_move":
                await self.socket_server.send_cmd(game_client, "play", "undo_move", data)
            case "surrender":
                await self.socket_server.send_cmd(game_client, "play", "surrender", data)
            case "quit":
                await self.socket_server.send_cmd(game_client, "play", "quit", data)
            case "new_game":
                await self.socket_server.send_cmd(game_client, "play", "new_game", data)
            case "blunder":
                await self.socket_server.send_cmd(game_client, "play", "blunder", data)
            case "timeline":
                await self.socket_server.send_cmd(game_client, "play", "timeline", data)
            case "step":
                await self.socket_server.send_cmd(game_client, "play", "step", data)
            case "unstep":
                await self.socket_server.send_cmd(game_client, "play", "unstep", data)
            case "evaluate":
                data.update({"mode": "playerai_vs_ai"})
                await self.socket_server.send_cmd(game_client, "play", "evaluate", data)
            case "stop_evaluate":
                await self.socket_server.send_cmd(game_client, "play", "stop_evaluate", data)
            case _:
                await self.send_response(client, EResponse.ERROR, f"Command '{command_key}' not found!")
