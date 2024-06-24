from enum import Enum


class RCODE(Enum):
    # General
    INTERNALERROR = 50
    INVALIDJSON = 51
    COMMANDNOTFOUND = 52
    INVALIDLANGUAGE = 53

    # success
    LANGUAGECHANGED = 0

    # Lobby success
    L_CREATED = 100  # "The lobby has been successfully created."
    L_JOINED = 101  # "The player has successfully joined the lobby."
    L_LEFT = 102  # "The player has successfully left the lobby."
    L_SWAPPED = 103  # "The player has successfully swapped positions within the lobby."
    L_POS = 104  # "The current position in the lobby has been successfully retrieved."
    L_STATUS = 105  # "The status of the lobby has been successfully retrieved."

    # Lobby error
    L_CLIENTALREADYINLOBBY = 150  # "Client already in a lobby. Client can not join multiple lobby at the same time."
    L_LOBBYNOTEXIST = 151  # "The specified lobby does not exist."
    L_JOINFAILURE = 152  # "The attempt to join the lobby has failed."
    L_CLIENTNOTINLOBBY = 153  # "The specified client does not exist."
    L_POSUNKNOWN = 154  # "The position within the lobby is unknown."
    L_POSOCCUPIED = 155  # "The position within the lobby is already occupied."
    L_LOBBYKEYINVALID = 156        # "There is an error with the lobby key, such as an invalid or missing key."
    # L_LOBBYNOTREADY = 157          # "Lobby does not have enough players to start!"

    # Play success
    P_ARENAINIT = 200  # "The Arena has been successfully initialized."
    #P_EVAL = 201  #"The play evaluation has been successfully performed."
    P_GAMEOVER = 202  # "The game has ended successfully."
    #P_EVALOVER = 203  # "The evaluation process has concluded successfully."
    #P_BOARD = 205  # "The game board has been successfully retrieved or updated."
    #P_REPRESENTATION = 206  # "The game representation has been successfully retrieved."
    P_VALIDMOVE = 207  # "A valid move has been made."
    P_MOVES = 208  # "The list of possible moves has been successfully retrieved."
    P_VALIDUNDO = 209  # "A valid undo action has been performed."
    P_SURRENDER = 210  # "A player has surrendered successfully."
    #P_BLUNDER = 212  # "A blunder [serious mistake] has been identified in the play."
    #P_BLUNDERLIST = 213  # "The list of blunders has been successfully retrieved."
    P_TIMELINE = 214  # "The timeline of events in the game has been successfully retrieved."
    #P_GAMES = 215  # "The list of games has been successfully retrieved."
    P_NOVALIDMOVES = 216  # The Player does not have a valid move anymore
    P_STEP = 217
    P_UNSTEP = 218
    P_PLAYER = 219  # sends the current active player


    # Play error
    P_NOGAMECLIENT = 250  # "There is no game client available. Try again."
    P_NOPERMISSION = 251  # "The player does not have permission to perform the action."
    P_NOTRUNNING = 252  # "The game has not been initialized."
    P_ARGS = 253  # "The arguments provided are invalid."
    P_STILLRUNNING = 254  # "The game is still running and the requested action cannot be performed."
    P_NOMOVE = 255  # "No move has been made."
    P_INVALIDMOVE = 256  # "The move made is invalid."
    P_INVALIDPOS = 257  # "The position specified is invalid."
    P_NOUNDO = 258  # "No undo action is available."
    P_INVALIDUNDO = 259  # "The undo action attempted is invalid."
    P_NOTIMELINE = 260  # "No timeline is available."
    P_INVALIDTIMELINE = 261  # "The timeline specified is invalid."
    P_NOEVALUATION = 262  # "No evaluation is available."
    P_INVALIDEVALUATION = 263  # "The evaluation attempted is invalid."
    #P_NOAVAILABLEGAMES = 264  # "No games are available."
    P_GAMENOTAVAILABLE = 265  # "The specified game is not available."
    P_NOGAMEINIT = 267  # Create a game fist.
    P_EVALNUMOVER = 268  # The selected num is too high

    # Debug
    D_CONTAINER = 300  # "List all active container!"
    D_TOGGLECLIENT = 301  # "Toggle debug mode of game_client"

    @staticmethod
    def get(code: int) -> "RCODE":
        for e in RCODE:
            if e.value == code:
                return e
