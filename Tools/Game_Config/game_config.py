from dataclasses import dataclass
from typing import Any

# Importing necessary enums and interfaces from the Tools.Game_Config module
from Tools.Game_Config.difficulty import EDifficulty
from Tools.Game_Config.mode import EGameMode
from Tools.i_game import IGame


@dataclass
class GameConfig:
    """
    A configuration class for game settings.

    Attributes:
        game_name (str): The name of the game.
        game (IGame): An instance of the game interface.
        mode (EGameMode): The game mode, which is an enum or class defined in the module.
        difficulty (EDifficulty): The game difficulty level, which is an enum or class defined in the module.
    """
    game_name: str = None
    game: IGame = None
    mode: 'EGameMode' = None  # Assuming EGameMode is a class or Enum defined elsewhere
    difficulty: 'EDifficulty' = None  # Assuming EDifficulty is a class or Enum defined elsewhere

    def ready(self) -> bool:
        """
        Checks if the game configuration is fully set up.

        Returns:
            bool: True if all attributes (game_name, game, mode, difficulty) are not None, False otherwise.
        """
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
        """
        Converts a dictionary to a GameConfig object.

        Args:
            read_object (dict[str, Any]): The dictionary containing the game configuration.
            game_list (dict[str, IGame]): A dictionary mapping game names to IGame instances.

        Returns:
            GameConfig: The populated GameConfig object.
        """
        # Extract the game name from the dictionary
        game_name = read_object.get("game")
        # Get the corresponding game instance from the game list
        game = game_list.get(game_name)
        # Get the mode and difficulty from the dictionary, using their respective get methods
        mode = EGameMode.get(read_object.get("mode"))
        difficulty = EDifficulty.get(read_object.get("difficulty"))
        # Return a new GameConfig instance with the extracted values
        return GameConfig(game_name, game, mode, difficulty)

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the GameConfig object to a dictionary.

        Returns:
            dict[str, Any]: The dictionary representation of the GameConfig object.
        """
        return {
            "game": self.game_name,
            # Use the name attribute of the mode and difficulty enums, if they are not None
            "mode": self.mode.name if self.mode else None,  # EGameMode has a name attribute
            "difficulty": self.difficulty.name if self.difficulty else None  # EDifficulty has a name attribute
        }
