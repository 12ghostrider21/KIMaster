class Player:
    def __init__(self):
        """
        Initializes a Player object with default attributes.

        Attributes:
            move (None or any): Represents the current move of the player.
                                Initially set to None indicating no move has been made yet.
            send (bool): A flag to indicate if a move has been sent. Initially set to False.
        """
        self.move = None
        self.send = False

    def play(self):
        """
        Processes and returns the current move of the player.

        This method retrieves the player's move, resets the move attribute to None,
        and then returns the move. If no move has been set (move is None), it returns None.

        Returns:
            temp (None or any): The move that was made by the player. If no move was made, returns None.
        """
        # Store the current move in a temporary variable
        temp = self.move
        # Reset the move to None, indicating the move has been processed
        self.move = None
        # If there was no move, return None
        if temp is None:
            return temp
        # Return the move that was made
        return temp

    def playAI(self):
        """
        Simulates an AI player making a move.

        This method checks the send flag to determine if a move should be made. If the flag is False,
        it sets it to True and returns True, indicating an AI move should be made. If the flag is True,
        it processes and returns the current move, resets the move attribute to None, and sets the
        send flag back to False.

        Returns:
            (bool or any): If the send flag was initially False, returns True to indicate an AI move.
                           Otherwise, returns the move made by the AI. If no move was made, returns None.
        """
        # If the send flag is not set, set it and return True indicating an AI move
        if not self.send:
            self.send = True
            return True
        # Store the current move in a temporary variable
        temp = self.move
        # Reset the move to None, indicating the move has been processed
        self.move = None
        # If there was no move, return None
        if temp is None:
            return temp
        # Reset the send flag to False after processing the move
        self.send = False
        # Return the move that was made
        return temp
