from enum import Enum


# Define an enumeration for response codes (RCODE) used to indicate various statuses and errors
class RCODE(Enum):
    # General success codes
    LANGUAGECHANGED = 0  # Language has been successfully changed
    INVALIDLANGUAGE = 1  # The specified language does not exist

    # General error codes
    INTERNALERROR = 50  # Critical internal error
    INVALIDJSON = 51  # The received message is not a valid JSON
    COMMANDNOTFOUND = 52  # The specified command does not exist
    INVALIDGAME = 53  # The specified game does not exist
    INVALIDDIFFICULTY = 54  # The specified difficulty level does not exist
    INVALIDMODE = 55  # The specified game mode does not exist

    # Lobby success codes
    L_CREATED = 100  # Lobby has been successfully created
    L_JOINED = 101  # Player has successfully joined the lobby
    L_LEFT = 102  # Player has successfully left the lobby
    L_SWAPPED = 103  # Player has successfully swapped positions within the lobby
    L_POS = 104  # Current position in the lobby has been successfully retrieved
    L_STATUS = 105  # Lobby status has been successfully retrieved
    L_GAMES = 106  # List of games has been successfully retrieved

    # Lobby error codes
    L_CLIENTALREADYINLOBBY = 150  # Client is already in a lobby and cannot join multiple lobbies
    L_LOBBYNOTEXIST = 151  # The specified lobby does not exist
    L_JOINFAILURE = 152  # Failed to join the lobby
    L_CLIENTNOTINLOBBY = 153  # The specified client is not in the lobby
    L_POSUNKNOWN = 154  # The position within the lobby is unknown
    L_POSOCCUPIED = 155  # The position within the lobby is already occupied
    L_LOBBYKEYINVALID = 156  # Invalid or missing lobby key
    L_LOBBYNOTREADY = 157  # Lobby does not have enough players to start
    L_NOLEAVEACTIVPLAYER = 158  # Client cannot leave an active game as a player
    L_NOSWAP = 159  # Client cannot swap positions in an active game as a player
    L_RUNNINGNOJOIN = 160  # Lobby is already running; join only as a spectator

    # Play success codes
    P_ARENAINIT = 200  # Arena has been successfully initialized
    P_EVAL = 201  # Play evaluation has been successfully performed
    P_GAMEOVER = 202  # Game has ended successfully
    P_EVALOVER = 203  # Evaluation process has concluded successfully
    P_BOARD = 205  # Game board has been successfully retrieved or updated
    P_REPRESENTATION = 206  # Game representation has been successfully retrieved
    P_VALIDMOVE = 207  # A valid move has been made
    P_MOVES = 208  # List of possible moves has been successfully retrieved
    P_VALIDUNDO = 209  # A valid undo action has been performed
    P_SURRENDER = 210  # A player has surrendered successfully
    P_BLUNDER = 211  # A blunder (serious mistake) has been identified in the play
    P_BLUNDERLIST = 212  # List of blunders has been successfully retrieved
    P_TIMELINE = 214  # Timeline of events in the game has been successfully retrieved
    P_NOVALIDMOVES = 215  # Player does not have any valid moves left
    P_STEP = 216  # Step forward in the timeline
    P_UNSTEP = 217  # Step backward in the timeline
    P_PLAYER = 218  # Sends the current active player

    # Play error codes
    P_NOGAMECLIENT = 250  # No game client available; try again
    P_NOPERMISSION = 251  # Player does not have permission to perform the action
    P_NOTRUNNING = 252  # Game has not been initialized
    P_ARGS = 253  # Invalid arguments provided
    P_STILLRUNNING = 254  # Game is still running; requested action cannot be performed
    P_NOMOVE = 255  # No move has been made
    P_INVALIDMOVE = 256  # The move made is invalid
    P_INVALIDPOS = 257  # The specified position is invalid
    P_NOUNDO = 258  # No undo action available
    P_INVALIDUNDO = 259  # The undo action attempted is invalid
    P_NOTIMELINE = 260  # No timeline available
    P_INVALIDTIMELINE = 261  # The specified timeline is invalid
    P_NOEVALUATION = 262  # No evaluation available
    P_INVALIDEVALUATION = 263  # The evaluation attempted is invalid
    P_GAMENOTAVAILABLE = 265  # The specified game is not available
    P_NOGAMEINIT = 266  # Create a game first
    P_EVALNUMOVER = 267  # The selected number is too high
    P_NOTYOURTURN = 268  # Player tried to make a move out of turn

    # Debug codes
    D_CONTAINER = 300  # List all active containers
    D_TOGGLECLIENT = 301  # Toggle debug mode of the game client

    # Static method to get the enumeration member by its value
    @staticmethod
    def get(code: int) -> "RCODE":
        # Iterate over all enumeration members
        for e in RCODE:
            # Check if the value of the enumeration member matches the given code
            if e.value == code:
                return e  # Return the matching enumeration member
