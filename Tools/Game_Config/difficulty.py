from enum import Enum


# Define an enumeration to represent different difficulty levels
class EDifficulty(Enum):
    # Each difficulty level is associated with a numeric value
    easy = 2
    medium = 35
    hard = 100

    @staticmethod
    def get(difficulty: str):
        """
        Static method to retrieve the EDifficulty enum member based on a string input.

        Args:
            difficulty (str): The difficulty level as a string ('easy', 'medium', 'hard').

        Returns:
            EDifficulty: The corresponding EDifficulty enum member if found, else None.
        """
        # Return None if the input difficulty string is None
        if difficulty is None:
            return None
        # Iterate over each member in the EDifficulty enumeration
        for m in EDifficulty:
            # Compare the input string with the name of the enum member (case-insensitive)
            if m.name.lower() == difficulty.lower():
                # Return the matching enum member
                return m
        # Return None if no match is found
        return None
