from enum import Enum
from dataclasses import dataclass
from Tools.Game_Config import Entry, EGameMode, EDifficulty


@dataclass
class GameConfig:
    game: Entry | Enum = None
    mode: EGameMode | Enum = None
    difficulty: EDifficulty | Enum = None

    def __call__(self) -> bool:
        if self.game is None:
            return False
        if self.mode is None:
            return False
        if self.difficulty is None:
            return False
        return True
