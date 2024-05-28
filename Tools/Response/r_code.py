from enum import Enum
from .r_text import RText


class R_CODE(Enum):
    # General success = 0 - 50

    # General error = 50 - 100
    COMMANDNOTFOUND = RText(50, "System is unable to find the command.")
    NONVALIDJSON = RText(51, "This error indicates that the JSON data provided is not valid.")
    INTERNALERROR = RText(52, "This represents an internal system error."
                              " It is a generic error that suggests something went wrong within the system.")

    # Lobby success = 100 -150
    LS_CREATED = RText(100, "The lobby has been successfully created.")
    L_JOINED = RText(101, "The player has successfully joined the lobby.")
    L_LEFT = RText(102, "The player has successfully left the lobby.")
    L_SWAPPED = RText(103, "The player has successfully swapped positions within the lobby.")
    L_POS = RText(104, "The current position in the lobby has been successfully retrieved.")
    L_STATUS = RText(105, "The status of the lobby has been successfully retrieved.")

    # Lobby error 150 - 200
    L_CLIENTINLOBBY = RText(150, "Client already in a lobby. Client can not join multiple lobby at the same time.")
    L_LOBBYNOTEXIST = RText(151, "The specified lobby does not exist.")
    L_JOINFAILURE = RText(152, "The attempt to join the lobby has failed.")
    L_CLIENTNOTEXIST = RText(153, "The specified client does not exist.")
    L_POSUNKNOWN = RText(154, "The position within the lobby is unknown.")
    L_POSOCCUPIED = RText(155, "The position within the lobby is already occupied.")
    L_LOBBYKEY = RText(156, "There is an error with the lobby key, such as an invalid or missing key.")
    L_LOBBYNOTREADY = RText(157, "Lobby does not have enough players to start!")

    # Play success = 200 - 250
    P_INIT = RText(200, "The play has been successfully initialized.")
    P_EVAL = RText(201, "The play evaluation has been successfully performed.")
    P_GAMEOVER = RText(202, "The game has ended successfully.")
    P_EVALOVER = RText(203, "The evaluation process has concluded successfully.")
    # P_TURN = RText(204, "Turn")  # currently not needed
    P_BOARD = RText(205, "The game board has been successfully retrieved or updated.")
    P_REPRESENTATION = RText(206, "The game representation has been successfully retrieved.")
    P_VALIDMOVE = RText(207, "A valid move has been made.")
    P_MOVES = RText(208, "The list of possible moves has been successfully retrieved.")
    P_VALIDUNDO = RText(209, "A valid undo action has been performed.")
    P_SURRENDER = RText(210, "A player has surrendered successfully.")
    P_BLUNDER = RText(212, "A blunder (serious mistake) has been identified in the play.")
    P_BLUNDERLIST = RText(213, "The list of blunders has been successfully retrieved.")
    P_TIMELINE = RText(214, "The timeline of events in the game has been successfully retrieved.")
    P_GAMES = RText(215, "The list of games has been successfully retrieved.")

    # Play error = 250 - 300
    P_NOGAMECLIENT = RText(250, "There is no game client available. Try again.")
    P_NOPERMISSION = RText(251, "The player does not have permission to perform the action.")
    P_NOINIT = RText(252, "The game has not been initialized.")
    P_ARGS = RText(253, "The arguments provided are invalid.")
    P_STILLRUNNING = RText(254, "The game is still running and the requested action cannot be performed.")
    P_NOMOVE = RText(255, "No move has been made.")
    P_INVALIDMOVE = RText(256, "The move made is invalid.")
    P_INVALIDPOS = RText(257, "The position specified is invalid.")
    P_NOUNDO = RText(258, "No undo action is available.")
    P_INVALIDUNDO = RText(259, "The undo action attempted is invalid.")
    P_NOTIMELINE = RText(260, "No timeline is available.")
    P_INVALIDTIMELINE = RText(261, "The timeline specified is invalid.")
    P_NOEVALUATION = RText(262, "No evaluation is available.")
    P_INVALIDEVALUATION = RText(263, "The evaluation attempted is invalid.")
    P_NOAVAILABLEGAMES = RText(264, "No games are available.")
    P_GAMENOTAWAILABLE = RText(265, "The specified game is not available.")

    # Debug success = 300 - 350
    D_CONTAINER = RText(300, "The debug container has been successfully created or accessed.")
    D_TOGGLE = RText(301, "The debug toggle action has been successfully performed.")

    # Debug error = 350 - 400


