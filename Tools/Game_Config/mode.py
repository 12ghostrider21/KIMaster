from enum import Enum

# Define an enumeration for different game modes
class EGameMode(Enum):
    # Player vs Player mode
    player_vs_player = 0
    # Player vs Kim (an AI or specific character) mode
    player_vs_kim = 1
    # Kim vs Player mode (Kim starts or is in control first)
    kim_vs_player = 2
    # AI Player vs AI Player mode
    playerai_vs_playerai = 3
    # AI Player vs Kim mode
    playerai_vs_kim = 4
    # Kim vs AI Player mode
    kim_vs_playerai = 5

    # Static method to get the corresponding game mode from a string
    @staticmethod
    def get(mode: str):
        # If no mode is provided, return None
        if mode is None:
            return None
        # Iterate through all possible game modes
        for m in EGameMode:
            # Check if the mode name matches the provided string (case insensitive)
            if m.name.lower() == mode.lower():
                # Return the matching game mode
                return m
        # If no match is found, return None
        return None
