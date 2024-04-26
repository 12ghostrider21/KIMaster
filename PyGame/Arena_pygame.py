import pygame

from IPlayer import IPlayer
from IGame import IGame


class Arena:
    def __init__(self, player1: IPlayer, player2: IPlayer, game: IGame):
        self.player1: IPlayer = player1
        self.player2: IPlayer = player2
        self.game: IGame = game
        pygame.init()  # starting pygame instance

        CUSTOM_EVENT_1 = pygame.USEREVENT + 1
        custom_event1 = pygame.event.Event(CUSTOM_EVENT_1, data={"key": "value"})

    def playGame(self):
        # Game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                print(event)


if __name__ == "__main__":
    from TicTacToePlayers import HumanTicTacToePlayer
    from TicTacToeGame import TicTacToeGame
    g = TicTacToeGame()
    p1 = HumanTicTacToePlayer(g)
    p2 = HumanTicTacToePlayer(g)
    a = Arena(p1, p2, g)
    a.playGame()