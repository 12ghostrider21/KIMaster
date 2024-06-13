from dataclasses import dataclass
from typing import Any

from Tools.Game_Config.difficulty import EDifficulty
from Tools.Game_Config.mode import EGameMode


@dataclass
class GameConfig:
    game: str = None
    mode: 'EGameMode' = None  # Assuming EGameMode is a class or Enum defined elsewhere
    difficulty: 'EDifficulty' = None  # Assuming EDifficulty is a class or Enum defined elsewhere

    def ready(self) -> bool:
        if self.game is None:
            return False
        if self.mode is None:
            return False
        if self.difficulty is None:
            return False
        return True

    @staticmethod
    def dict_to_config(read_object: dict[str, Any]) -> 'GameConfig':
        game = read_object.get("game")
        mode = EGameMode.get(read_object.get("mode"))
        difficulty = EDifficulty.get(read_object.get("difficulty"))
        return GameConfig(game, mode, difficulty)

    def to_dict(self) -> dict[str, Any]:
        return {
            "game": self.game,
            "mode": self.mode.name if self.mode else None,  # Assuming EGameMode has a name attribute
            "difficulty": self.difficulty.name if self.difficulty else None  # Assuming EDifficulty has a name attribute
        }
