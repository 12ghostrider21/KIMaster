from enum import Enum


class R_CODE(Enum):
    # General success = 0 - 50

    # General error = 50 - 100
    COMMANDNOTFOUND = 50
    NONVALIDJSON = 51
    INTERNALERROR = 52

    # Lobby success = 100 -150
    L_CREATED = 100
    L_JOINED = 101
    L_LEFT = 102
    L_SWAPPED = 103
    L_POS = 104
    L_STATUS = 105

    # Lobby error 150 - 200
    L_CLIENT = 150
    L_LOBBYNOTEXIST = 151
    L_JOINFAILURE = 152
    L_CLIENTNOTEXIST = 153
    L_POSUNKNOWN = 154
    L_POSOCCUPIED = 155
    L_LOBBYKEY = 156

    # Play success = 200 - 250
    P_INIT = 200
    P_EVAL = 201
    P_GAMEOVER = 202
    P_EVALOVER = 203
    # P_TURN = 204  # currently not needed
    P_BOARD = 205
    P_REPRESENTATION = 206
    P_VALIDMOVE = 207
    P_MOVES = 208
    P_VALIDUNDO = 209
    P_SURRENDER = 210
    P_QUIT = 211
    P_BLUNDER = 212
    P_BLUNDERLIST = 213
    P_TIMELINE = 214

    # Play error = 250 - 300
    P_NOGAMECLIENT = 250
    P_NOPERMISSION = 251
    P_NOINIT = 252
    P_ARGS = 253
    P_STILLRUNNING = 254
    P_NOMOVE = 255
    P_INVALIDMOVE = 256
    P_INVALIDPOS = 257
    P_NOUNDO = 258
    P_INVALIDUNDO = 259
    P_NOTIMELINE = 260
    P_INVALIDTIMELINE = 261
    P_NOEVALUATION = 262
    P_INVALIDEVALUATION = 263

    # Debug success = 300 - 350
    D_CONTAINER = 300
    D_TOGGLE = 301

    # Debug error = 350 - 400