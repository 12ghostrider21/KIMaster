import logging

from tqdm import tqdm

log = logging.getLogger(__name__)


class Arena:
    """
    An Arena class where any 2 agents can be pit against each other.
    """

    def __init__(self, player1, player2, game, display=None):
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
        self.display = display

    def playGame(self, verbose=False):
        """
        Executes one episode of a game.

        Returns:
            either
                winner: player who won the game (1 if player1, -1 if player2)
            or
                draw result returned from the game that is neither 1, -1, nor 0.
        """
        players = [self.player2, None, self.player1]
        cur_player = 1
        board = self.game.getInitBoard()
        #print(self.game.drawTerminal(board, False, cur_player))
        it = 0

        for player in players[0], players[2]:
            if hasattr(player, "startGame"):
                player.startGame()

        while self.game.getGameEnded(board, cur_player) == 0:
            it += 1
            if verbose:
                assert self.display
                print("Turn ", str(it), "Player ", str(cur_player))
                self.display(board)
            action = players[cur_player + 1](board, cur_player)

            # Notifying the opponent for the move
            opponent = players[-cur_player + 1]
            if hasattr(opponent, "notify"):
                opponent.notify(board, action)
            #print("cur_playerArena", cur_player)

            converted_action = self.game.translate(board, cur_player, action)  # ai generated "move" is just an index
            board, cur_player = self.game.getNextState(board, cur_player, converted_action)
            #print(self.game.drawTerminal(board, False, cur_player))

        for player in players[0], players[2]:
            if hasattr(player, "endGame"):
                player.endGame()

        if verbose:
            assert self.display
            print("Game over: Turn ", str(it), "Result ", str(cur_player * self.game.getGameEnded(board, cur_player)))
            self.display(board)

        return cur_player * self.game.getGameEnded(board, cur_player)

    def playGames(self, num, verbose=False):
        """
        Plays num games in which player1 starts num/2 games and player2 starts
        num/2 games.

        Returns:
            one_won: games won by player1
            two_won: games won by player2
            draws:  games won by nobody
        """

        num = int(num / 2)
        one_won = 0
        two_won = 0
        draws = 0
        for _ in tqdm(range(num), desc="Arena.playGames (1)"):
            game_result = self.playGame(verbose=verbose)
            if game_result == 1:
                one_won += 1
            elif game_result == -1:
                two_won += 1
            else:
                draws += 1

        self.player1, self.player2 = self.player2, self.player1

        for _ in tqdm(range(num), desc="Arena.playGames (2)"):
            game_result = self.playGame(verbose=verbose)
            if game_result == -1:
                one_won += 1
            elif game_result == 1:
                two_won += 1
            else:
                draws += 1

        return one_won, two_won, draws
