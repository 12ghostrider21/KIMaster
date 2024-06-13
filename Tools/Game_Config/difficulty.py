from enum import Enum


class EDifficulty(Enum):
    easy = 2
    medium = 10
    hard = 50

    @staticmethod
    def get(difficulty: str):
        if difficulty is None:
            return None
        for m in EDifficulty:
            if m.name.lower() == difficulty.lower():
                return m
        return None