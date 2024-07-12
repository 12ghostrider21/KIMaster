# External imports
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import WebSocket, WebSocketDisconnect
from json import loads, JSONDecodeError

# Own modules
from Server.connection_manager import AbstractConnectionManager
from Server.lobby import Lobby
from Server.lobby_manager import LobbyManager
from Tools.Game_Config.difficulty import EDifficulty
from Tools.Game_Config.mode import EGameMode
from Tools.dynamic_imports import Importer
from Tools.language_handler import LanguageHandler, LANGUAGE
from Tools.rcode import RCODE


class FastAPIServer(AbstractConnectionManager):
    """
    FastAPI Server class to manage WebSocket connections, lobby, and game interactions.

    Attributes:
        manager (LobbyManager): Manages lobbies.
        importer (Importer): Imports game configurations.
        executor (ThreadPoolExecutor): Thread pool executor for asynchronous tasks.
        __command_mask (list[str]): List of allowed command keys.
        __play_mask (list[str]): List of allowed play command keys.
    """
    def __init__(self, manager: LobbyManager, msg_builder: LanguageHandler, importer: Importer):
        """
        Initializes the FastAPIServer with given managers and handlers.

        Args:
            manager (LobbyManager): Manages lobbies.
            msg_builder (LanguageHandler): Handles language-based messages.
            importer (Importer): Imports game configurations.
        """
        super().__init__(msg_builder)
        self.manager: LobbyManager = manager
        self.importer: Importer = importer
        self.executor = ThreadPoolExecutor()  # Global Thread Executor without any Thread limits
        self.__command_mask: list[str] = ["command", "command_key", "pos", "key", "mode", "game", "difficulty", "num",
                                          "move", "lang", "fromPos", "isFrontend"]
        self.__play_mask: list[str] = ["create", "valid_moves", "make_move", "undo_move", "surrender",
                                       "new_game", "blunder", "timeline", "step", "unstep", "image"]

    async def connect(self, websocket: WebSocket):
        """
        Connects a WebSocket client.

        Args:
            websocket (WebSocket): The WebSocket connection to the client.
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        """
        Disconnects a WebSocket client and performs necessary clean-up.

        Args:
            websocket (WebSocket): The WebSocket connection to the client.
        """
        if websocket in self.active_connections:
            lobby: Lobby = self.manager.get_lobby(websocket)  # Get the lobby the client is part of
            if lobby is not None:
                if self.manager.get_pos_of_client(websocket) != "sp":
                    if lobby.game_running:  # If a game is running, handle surrender on connection loss
                        await self.send_cmd(game_client=lobby.game_client,
                                            command="play",
                                            command_key="surrender",
                                            data={"p_pos": self.manager.get_pos_of_client(websocket), "key": lobby.key})
                        lobby.game_running = False  # Override running mode for unresolved surrender
            self.active_connections.remove(websocket)  # Remove client from active connections
        self.manager.leave_lobby(websocket)  # Remove client from lobby
        self.msg_builder.remove_client(websocket)  # Remove client from private language selections

    async def websocket_endpoint(self, client: WebSocket):
        """
        Main endpoint for WebSocket connections, handling incoming messages.

        Args:
            client (WebSocket): The WebSocket connection to the client.
        """
        await self.connect(client)
        loop = asyncio.get_event_loop()  # Event loop for threading (each connection gets its own)
        try:
            while True:
                try:
                    read_object = await client.receive_json()  # Receive JSON data from the client
                    if isinstance(read_object, str):
                        read_object = loads(read_object)
                    # Filter read_object based on allowed keys
                    read_object = {k: v for k, v in read_object.items() if k in self.__command_mask}
                except JSONDecodeError:
                    await self.send_response(client, RCODE.INVALIDJSON)
                    continue

                command = read_object.get("command")
                match command:
                    case "debug":
                        self.submit_task(loop, self.handle_debug_command, client, read_object)
                    case "lobby":
                        self.submit_task(loop, self.handle_lobby, client, read_object)
                    case "play":
                        self.submit_task(loop, self.handle_play_command, client, read_object)
                    case "client":
                        self.submit_task(loop, self.handle_client, client, read_object)
                    case _:
                        await self.send_response(client, RCODE.COMMANDNOTFOUND, {"command": command})
        except WebSocketDisconnect as e:
            code = {1000: "Normal disconnect", 1001: "Browser reload/tab close", 1006: "Critical connection break!"}
            print(client.client, f"WebSocket disconnected with code: {e.code}, {code.get(e.code)}")
        finally:
            await self.disconnect(client)

    def submit_task(self, loop, coro, *args):
        """
        Run async methods in an own thread to reduce response times.

        Args:
            loop: Event loop.
            coro: Coroutine to run.
            *args: Parameters of coroutine.

        Returns: None
        """
        loop.run_in_executor(self.executor, lambda: asyncio.run(coro(*args)))

    async def handle_debug_command(self, client: WebSocket, read_object: dict):
        """
        Handles debug commands received from the client.

        Args:
            client (WebSocket): The WebSocket connection to the client.
            read_object (dict): The received command object.
        """
        command_key = read_object.get("command_key")
        match command_key:
            case "active_container":
                await self.send_response(client=client, code=RCODE.D_CONTAINER,
                                         data=self.manager.docker.list_containers())
            case "game_client":
                self.manager.docker.debug = not self.manager.docker.debug
                await self.send_response(client=client, code=RCODE.D_TOGGLECLIENT,
                                         data={"debug": self.manager.docker.debug})
            case _:
                await self.send_response(client=client, code=RCODE.COMMANDNOTFOUND, data={"command": command_key})

    async def handle_lobby(self, client: WebSocket, read_object: dict):
        """
        Handles lobby commands received from the client.

        Args:
            client (WebSocket): The WebSocket connection to the client.
            read_object (dict): The received command object.
        """
        command_key = read_object.get("command_key")
        match command_key:
            case "create":
                lobby = self.manager.get_lobby(client)
                if lobby:
                    return await self.send_response(client=client, code=RCODE.L_CLIENTALREADYINLOBBY)
                new_lobby_key = self.manager.create_lobby()
                self.manager.join_lobby(new_lobby_key, client, "p1")
                await self.send_response(client=client, code=RCODE.L_CREATED, data={"key": new_lobby_key})
            case "join":
                lobby_key = read_object.get("key")
                lobby: Lobby = self.manager.get_lobby(lobby_key)
                if lobby is None:
                    return await self.send_response(client=client, code=RCODE.L_LOBBYNOTEXIST, data={"key": lobby_key})
                lobby_key = read_object.get("key")
                pos = read_object.get("pos")
                if lobby.game_running:
                    if pos != "sp":
                        return await self.send_response(client=client, code=RCODE.L_RUNNINGNOJOIN)
                    else:  # pos is sp
                        await self.send_cmd(game_client=lobby.game_client,
                                            command="",
                                            command_key="image")
                if not self.manager.join_lobby(lobby_key, client, pos):
                    return await self.send_response(client=client, code=RCODE.L_CLIENTALREADYINLOBBY,
                                                    data={"key": lobby_key})
                await self.broadcast_response(client_list=lobby.get(None), code=RCODE.L_JOINED,
                                              data={"pos": self.manager.get_pos_of_client(client)})
            case "leave":
                lobby: Lobby = self.manager.get_lobby(client)
                if lobby is None:
                    return await self.send_response(client=client, code=RCODE.L_CLIENTNOTINLOBBY)
                pos = self.manager.get_pos_of_client(client)
                client_list = lobby.get(None)
                if not self.manager.leave_lobby(client):
                    if lobby.game_running and lobby.in_lobby(client):
                        return await self.send_response(client=client, code=RCODE.L_NOLEAVEACTIVPLAYER)
                await self.broadcast_response(client_list=client_list, code=RCODE.L_LEFT,
                                              data={"pos": pos})
            case "swap":
                pos: str = read_object.get("pos")
                lobby: Lobby = self.manager.get_lobby(client)
                if lobby is None:
                    return await self.send_response(client=client, code=RCODE.L_CLIENTNOTINLOBBY)
                if lobby.game_running:
                    if lobby.in_lobby(client):
                        return await self.send_response(client=client, code=RCODE.L_NOSWAP)
                if pos not in ["p1", "p2", "sp"]:
                    return await self.send_response(client=client, code=RCODE.L_POSUNKNOWN, data={"pos": pos})
                if not self.manager.swap_to(pos, client):
                    return await self.send_response(client=client, code=RCODE.L_POSOCCUPIED, data={"pos": pos})
                await self.broadcast_response(client_list=lobby.get(None), code=RCODE.L_SWAPPED, data={"pos": pos})
            case "pos":
                pos: str = self.manager.get_pos_of_client(client)
                if pos:
                    await self.send_response(client=client, code=RCODE.L_POS, data={"pos": pos})
                else:  # client not in lobby
                    await self.send_response(client=client, code=RCODE.L_CLIENTNOTINLOBBY)
            case "status":
                lobby: Lobby = self.manager.get_lobby(client)
                if lobby:  # success
                    await self.send_response(client=client, code=RCODE.L_STATUS, data=lobby.status())
                else:  # client not in lobby
                    await self.send_response(client=client, code=RCODE.L_CLIENTNOTINLOBBY)
            case "games":
                lobby: Lobby = self.manager.get_lobby(client)
                if lobby:  # success
                    await self.send_response(client=client, code=RCODE.L_GAMES,
                                             data={"games": [k for k in self.importer.get_games().keys()]})
                else:  # client not in lobby
                    await self.send_response(client=client, code=RCODE.L_CLIENTNOTINLOBBY)
            case _:
                await self.send_response(client=client, code=RCODE.COMMANDNOTFOUND, data={"command_key": command_key})

    async def handle_play_command(self, client: WebSocket, read_object: dict):
        """
        Handles play commands received from the client.

        Args:
            client (WebSocket): The WebSocket connection to the client.
            read_object (dict): The received command object.
        """
        lobby = self.manager.get_lobby(client)
        if lobby is None:
            return await self.send_response(client=client, code=RCODE.L_CLIENTNOTINLOBBY)
        if not lobby.game_client:
            return await self.send_response(client=client, code=RCODE.P_NOGAMECLIENT)
        pos: str = self.manager.get_pos_of_client(client)
        if pos == "sp":
            return await self.send_response(client=client, code=RCODE.P_NOPERMISSION)
        data = {"p_pos": pos, "key": lobby.key, **read_object}
        command_key = read_object.get("command_key")
        if command_key not in self.__play_mask:
            return await self.send_response(client=client, code=RCODE.COMMANDNOTFOUND,
                                            data={"command_key": command_key})
        if command_key == "create":
            lobby.game = data.get("game")
            lobby.difficulty = EDifficulty.get(data.get("difficulty"))
            lobby.mode = EGameMode.get(data.get("mode"))
            if self.importer.get_games().get(lobby.game) is None:
                return await self.send_response(client=client, code=RCODE.INVALIDGAME,
                                                data={"game": data.get("game"),
                                                      "available": [m for m in self.importer.get_games().keys()]})
            if lobby.difficulty is None:
                return await self.send_response(client=client, code=RCODE.INVALIDDIFFICULTY,
                                                data={"difficulty": data.get("difficulty"),
                                                      "available": [m.name for m in EDifficulty]})
            if lobby.mode is None:
                return await self.send_response(client=client, code=RCODE.INVALIDMODE,
                                                data={"mode": data.get("mode"),
                                                      "available": [m.name for m in EGameMode]})

        if command_key in ["create", "new_game"]:  # prevent a game to start without enough players
            missing = []
            mode_checks = {
                0: [("P1", True, " not connected!"), ("P2", True, " not connected!")],  # player_vs_player
                1: [("P1", True, " not connected!"), ("P2", False, " needs to be empty!")],  # player_vs_KIM
                2: [("P1", False, " needs to be empty!"), ("P2", True, " not connected!")],  # KIM_vs_player
                3: [("P1", True, " not connected!"), ("P2", True, " not connected!")],  # playerai_vs_playerai
                4: [("P1", True, " not connected!"), ("P2", False, " needs to be empty!")],  # playerai_vs_KIM
                5: [("P1", False, " needs to be empty!"), ("P2", True, " not connected!")]  # KIM_vs_playerai
            }
            for player, should_be_connected, message in mode_checks.get(lobby.mode.value, []):
                if should_be_connected and getattr(lobby, player.lower()) is None:
                    missing.append([player, message])
                elif not should_be_connected and getattr(lobby, player.lower()) is not None:
                    missing.append([player, message])
            if missing:
                return await self.send_response(client=client,
                                                code=RCODE.L_LOBBYNOTREADY,
                                                data={i[0]: i[1] for i in missing})

        await self.send_cmd(lobby.game_client, "play", command_key, data)

    async def handle_client(self, client: WebSocket, read_object: dict):
        """
        Handles client-specific commands received from the client.

        Args:
            client (WebSocket): The WebSocket connection to the client.
            read_object (dict): The received command object.
        """
        command_key = read_object.get("command_key")
        match command_key:
            case "language":
                lang: str = read_object.get("lang")
                if lang is not None:
                    for e in LANGUAGE:
                        if e.name.lower() == lang.lower():
                            self.msg_builder.update_language(client, e)
                            await self.send_response(client, RCODE.LANGUAGECHANGED, {"lang": e.name})
                            return
                await self.send_response(client, RCODE.INVALIDLANGUAGE, {"lang": lang})
            case _:
                await self.send_response(client, RCODE.COMMANDNOTFOUND, {"command": command_key})
