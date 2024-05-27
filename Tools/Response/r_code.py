from enum import Enum
from .r_text import RText


class R_CODE(Enum):
    # General success = 0 - 50

    # General error = 50 - 100
    COMMANDNOTFOUND = RText(50, "Command not found")
    NONVALIDJSON = RText(51, "Non-valid JSON")
    INTERNALERROR = RText(52, "Internal error")
    GAMECLIENTQUIT = RText(53, "Game client quit")

    # Lobby success = 100 -150
    L_CREATED = RText(100, "Lobby created")
    L_JOINED = RText(101, "Lobby joined")
    L_LEFT = RText(102, "Lobby left")
    L_SWAPPED = RText(103, "Lobby swapped")
    L_POS = RText(104, "Lobby position")
    L_STATUS = RText(105, "Lobby status")

    # Lobby error 150 - 200
    L_CLIENT = RText(150, "Lobby client error")
    L_LOBBYNOTEXIST = RText(151, "Lobby does not exist")
    L_JOINFAILURE = RText(152, "Lobby join failure")
    L_CLIENTNOTEXIST = RText(153, "Client does not exist")
    L_POSUNKNOWN = RText(154, "Position unknown")
    L_POSOCCUPIED = RText(155, "Position occupied")
    L_LOBBYKEY = RText(156, "Lobby key error")

    # Play success = 200 - 250
    P_INIT = RText(200, "Play initialized")
    P_EVAL = RText(201, "Play evaluation")
    P_GAMEOVER = RText(202, "Game over")
    P_EVALOVER = RText(203, "Evaluation over")
    # P_TURN = RText(204, "Turn")  # currently not needed
    P_BOARD = RText(205, "Board")
    P_REPRESENTATION = RText(206, "Representation")
    P_VALIDMOVE = RText(207, "Valid move")
    P_MOVES = RText(208, "Moves")
    P_VALIDUNDO = RText(209, "Valid undo")
    P_SURRENDER = RText(210, "Surrender")
    P_QUIT = RText(211, "Quit")
    P_BLUNDER = RText(212, "Blunder")
    P_BLUNDERLIST = RText(213, "Blunder list")
    P_TIMELINE = RText(214, "Timeline")
    P_GAMES = RText(215, "Games")

    # Play error = 250 - 300
    P_NOGAMECLIENT = RText(250, "No game client")
    P_NOPERMISSION = RText(251, "No permission")
    P_NOINIT = RText(252, "No initialization")
    P_ARGS = RText(253, "Invalid arguments")
    P_STILLRUNNING = RText(254, "Still running")
    P_NOMOVE = RText(255, "No move")
    P_INVALIDMOVE = RText(256, "Invalid move")
    P_INVALIDPOS = RText(257, "Invalid position")
    P_NOUNDO = RText(258, "No undo available")
    P_INVALIDUNDO = RText(259, "Invalid undo")
    P_NOTIMELINE = RText(260, "No timeline")
    P_INVALIDTIMELINE = RText(261, "Invalid timeline")
    P_NOEVALUATION = RText(262, "No evaluation")
    P_INVALIDEVALUATION = RText(263, "Invalid evaluation")
    P_NOAVAILABLEGAMES = RText(264, "No available games")
    P_GAMENOTAWAILABLE = RText(265, "Game not available")

    # Debug success = 300 - 350
    D_CONTAINER = RText(300, "Debug container")
    D_TOGGLE = RText(301, "Debug toggle")

    # Debug error = 350 - 400
