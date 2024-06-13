from enum import Enum


class EGameMode(Enum):
    player_vs_player = 0
    player_vs_ai = 1
    ai_vs_player = 2
    playerai_vs_playerai = 3

    @staticmethod
    def get(mode: str):
        if mode is None:
            return None
        for m in EGameMode:
            if m.name.lower() == mode.lower():
                return m
        return None
