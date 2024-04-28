import logging

from tqdm import tqdm

log = logging.getLogger(__name__)


class Arena():
    """
    An Arena class where any 2 agents can be pit against each other.
    """

    def __init__(self, player1, player2, game, draw_terminal=None):
        """
        Input:
            player 1,2: two functions that takes board as input, return action
            game: Game object
            display: a function that takes board as input and prints it (e.g.
                     display in othello/OthelloGame). Is necessary for verbose
                     mode.

        see othello/OthelloPlayers.py for an example. See pit.py for pitting
        human players/other baselines with each other.
        """
        self.player1 = player1
        self.player2 = player2
        self.game = game
        self.draw_terminal = draw_terminal

    # an episode = 1 Game played
    def playGame(self, verbose=False):  # if set to True, board gets displayed
        """
        Executes one episode of a game.

        Returns:
            either
                winner: player who won the game (1 if player1, -1 if player2)
            or
                draw result returned from the game that is neither 1, -1, nor 0.
        """
        players = [self.player2, None, self.player1]  # player2 and player1 are functions (lambda)
        curPlayer = 1
        board = self.game.getInitBoard()
        it = 0
        while self.game.getGameEnded(board, curPlayer) == 0:  # 0 is if game is not finished
            it += 1
            if verbose:
                assert self.draw_terminal
                print("Turn ", str(it), "Player ", str(curPlayer))
                self.draw_terminal(self, board)
                self.game.draw(board)
            action = players[curPlayer + 1](self.game.getCanonicalForm(board, curPlayer))  # the canonicalForm of the
                        # board is the argument for the player function (lambda x : ... (x)) -> look into pit.py
                        # in pit.py the maximum value from the ActionProbabilites is getting chosen;
                        # players are at index 0 and 2 => therefore curPlayer + 1 ==> -1 + 1 = 0; 1 + 1 = 2

            valids = self.game.getValidMoves(self.game.getCanonicalForm(board, curPlayer), 1)

            if valids[action] == 0:
                log.error(f'Action {action} is not valid!')
                log.debug(f'valids = {valids}')
                assert valids[action] > 0
            board, curPlayer = self.game.getNextState(board, curPlayer, action)
        if verbose:
            assert self.draw_terminal
            print("Game over: Turn ", str(it), "Result ", str(self.game.getGameEnded(board, 1)))
            self.draw_terminal(self, board)
            self.game.draw(board)
        return curPlayer * self.game.getGameEnded(board, curPlayer)

    def playGames(self, num, verbose=False):
        """
        Plays num games in which player1 starts num/2 games and player2 starts        # says all
        num/2 games.

        Returns:
            oneWon: games won by player1
            twoWon: games won by player2
            draws:  games won by nobody
        """

        num = int(num / 2)
        oneWon = 0
        twoWon = 0
        draws = 0
        for _ in tqdm(range(num), desc="Arena.playGames (1)"):  # _ is a placeholder => used if there is no need of a var
            gameResult = self.playGame(verbose=verbose)         # inside loop
            if gameResult == 1:
                oneWon += 1
            elif gameResult == -1:
                twoWon += 1
            else:
                draws += 1

        self.player1, self.player2 = self.player2, self.player1

        for _ in tqdm(range(num), desc="Arena.playGames (2)"):
            gameResult = self.playGame(verbose=verbose)
            if gameResult == -1:
                oneWon += 1
            elif gameResult == 1:
                twoWon += 1
            else:
                draws += 1

        return oneWon, twoWon, draws
