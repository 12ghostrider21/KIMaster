from enum import Enum


class EGameMode(Enum):
    player_vs_player = 0
    player_vs_kim = 1
    kim_vs_player = 2
    playerai_vs_playerai = 3
    playerai_vs_kim = 4
    kim_vs_playerai = 5

    @staticmethod
    def get(mode: str):
        if mode is None:
            return None
        for m in EGameMode:
            if m.name.lower() == mode.lower():
                return m
        return None
