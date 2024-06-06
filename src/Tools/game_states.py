from enum import Enum, auto


class GAMESTATE(Enum):
    WAITING = auto()        # Game not started yet / idle
    RUNNING = auto()        # Game is running
    FINISHED = auto()       # Game is finished
    EVALUATE = auto()       # Evaluation mode

