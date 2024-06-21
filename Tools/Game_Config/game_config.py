from dataclasses import dataclass
from typing import Any

from Tools.Game_Config.difficulty import EDifficulty
from Tools.Game_Config.mode import EGameMode
from Tools.i_game import IGame


@dataclass
class GameConfig:
    game_name: str = None
    game: IGame = None
    mode: 'EGameMode' = None  # Assuming EGameMode is a class or Enum defined elsewhere
    difficulty: 'EDifficulty' = None  # Assuming EDifficulty is a class or Enum defined elsewhere

    def ready(self) -> bool:
        if self.game_name is None:
            return False
        if self.game is None:
            return False
        if self.mode is None:
            return False
        if self.difficulty is None:
            return False
        return True

    @staticmethod
    def dict_to_config(read_object: dict[str, Any], game_list: dict[str, IGame]) -> 'GameConfig':
        game_name = read_object.get("game")
        game = game_list.get(game_name)
        mode = EGameMode.get(read_object.get("mode"))
        difficulty = EDifficulty.get(read_object.get("difficulty"))
        return GameConfig(game_name, game, mode, difficulty)

    def to_dict(self) -> dict[str, Any]:
        return {
            "game": self.game_name,
            "mode": self.mode.name if self.mode else None,  # EGameMode has a name attribute
            "difficulty": self.difficulty.name if self.difficulty else None  # EDifficulty has a name attribute
        }
