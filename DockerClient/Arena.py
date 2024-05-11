import logging
import asyncio
from DockerClient import Player
import numpy as np
from Datatypes import RESPONSE
from tqdm import tqdm

log = logging.getLogger(__name__)


class Arena:
    """
    An Arena class where any 2 agents can be pit against each other.
    """

    def __init__(self, player1, player2, game, game_client=None):
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
        self.game_client = game_client
        self.stop = False
        self.stop_lock = asyncio.Lock()
        self.history = []  # (board, curPlayer, action, iterator)
        self.blunder_history = []  # (iterator, action)
        self.timeline_start: int = 0

    # an episode = 1 Game played
    async def playGame(self, verbose=False, eval=False, board=None, curPlayer: int = 1, it: int = 0):
        """
        Executes one episode of a game.

        Returns:
            either
                winner: player who won the game (1 if player1, -1 if player2)
            or
                draw result returned from the game that is neither 1, -1, nor 0.
        """
        players = [self.player2, None, self.player1]  # player2 and player1 are functions (lambda)
        if board is None:
            board = self.game.getInitBoard()
        while self.game.getGameEnded(board, curPlayer) == 0:  # 0 is if game is not finished
            if verbose and not eval:
                await self.game_client.send_cmd("play", "arena", {"response_code": RESPONSE.SUCCESS,
                                                                  "response_msg": "Player" + str(
                                                                      curPlayer) + "'s turn:"})
                representation = self.game.draw_terminal(board, False, curPlayer)
                await self.game_client.send_response(RESPONSE.SUCCESS, "img", {"payload": representation})
                img1, img2 = self.game.draw(board, False, curPlayer)
                await self.game_client.send_image(img1, img2)
            action = None
            if verbose:  # same as with blunder_history
                self.history.append((board, curPlayer, action, it))
            if isinstance(players[curPlayer + 1], type(Player.play)):  # user (AI) is in charge to make a turn
                user_action = players[curPlayer + 1](self.game.getCanonicalForm(board, curPlayer))  # the canonicalForm
                # of the board is the argument for the player function (lambda x : ... (x) / play(self,board))
                # players are at index 0 and 2 => curPlayer + 1 ==> -1 + 1 = 0; 1 + 1 = 2
                async with self.stop_lock:
                    if self.stop:
                        break
                if verbose:  # if evaluation is running (multiple games), blunder_history should not be created,
                    # except for the last game
                    ref_actions = players[-curPlayer + 1](self.game.getCanonicalForm(board, curPlayer)).sort()
                    upper_half = len(ref_actions) // 2
                    bad_actions = ref_actions[:upper_half]
                    for a in bad_actions:  # comparing move with rather bad moves for show_blunder function
                        if a == user_action:
                            self.blunder_history.append((it, user_action))
            else:  # website AI is in charge of making a turn
                action = np.argmax(players[curPlayer + 1](self.game.getCanonicalForm(board, curPlayer)))

            valids = self.game.getValidMoves(self.game.getCanonicalForm(board, curPlayer), 1)

            if valids[action] == 0:
                log.error(f'Action {action} is not valid!')
                log.debug(f'valids = {valids}')
                assert valids[action] > 0
            board, curPlayer = self.game.getNextState(board, curPlayer, action)
            it += 1
            await asyncio.sleep(0.1)
        if verbose and not eval:
            await self.game_client.send_cmd("play", "arena", {"response_code": RESPONSE.SUCCESS,
                                                              "response_msg": "Game over: Turn " + str(it) +
                                                                              "; Result: " + str(
                                                                  self.game.getGameEnded(board, 1))})
            representation = self.game.draw_terminal(board, False, curPlayer)
            await self.game_client.send_response(RESPONSE.SUCCESS, "img", {"payload": representation})
            img1, img2 = self.game.draw(board, False, curPlayer)
            await self.game_client.send_image(img1, img2)
        async with self.stop_lock:
            if self.stop:  # when giving up, stop_game is called as well => therefore (curPlayer * -1) is the winner
                self.stop = False
                return curPlayer * -1
        return curPlayer * self.game.getGameEnded(board, curPlayer)

    async def playGames(self, num):
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
        for i in tqdm(range(num), desc="Arena.playGames (1)"):
            if i == (num - 1):
                gameResult = self.playGame(verbose=True, eval=True)
                async with self.stop_lock:
                    if self.stop:
                        self.stop = False
                        return oneWon, twoWon, draws
            else:
                gameResult = self.playGame(verbose=False, eval=True)
                async with self.stop_lock:
                    if self.stop:
                        self.stop = False
                        return oneWon, twoWon, draws
            if gameResult == 1:
                oneWon += 1
            elif gameResult == -1:
                twoWon += 1
            else:
                draws += 1

        self.player1, self.player2 = self.player2, self.player1

        for i in tqdm(range(num), desc="Arena.playGames (2)"):
            if i == (num - 1):
                gameResult = self.playGame(verbose=True, eval=True)
                async with self.stop_lock:
                    if self.stop:
                        self.stop = False
                        return oneWon, twoWon, draws
            else:
                gameResult = self.playGame(verbose=False, eval=True)
                async with self.stop_lock:
                    if self.stop:
                        self.stop = False
                        return oneWon, twoWon, draws
            if gameResult == -1:
                oneWon += 1
            elif gameResult == 1:
                twoWon += 1
            else:
                draws += 1

        return oneWon, twoWon, draws

    async def stop_game(self, flag: bool = True):
        async with self.stop_lock:
            self.stop = flag

    async def undo_move(self, amount: int):
        if len(self.history) >= 3:  # otherwise the user would try to undo a move he hasn't done yet
            for _ in range(amount * 2):
                self.history.pop()
                if len(self.history) == 1:  # if hand in amount is too high ==> going back to at least init_state of
                    # the board
                    break
        await self.stop_game()
        tmp = self.history[-1]
        self.history.pop()  # additional pop because the same state is added in play again when calling play
        await self.game_client.send_response(RESPONSE.SUCCESS, "Move successfully undone")
        await self.playGame(board=tmp[-1][0], curPlayer=tmp[-1][1], it=tmp[-1][3])

    async def draw_valid_moves(self, from_pos: int):
        img1, img2 = self.game.draw(self.game.getCanonicalForm(self.history[-1][0], -1), True, -1, from_pos)
        await self.game_client.send_image(img1, img2)
        representation = self.game.draw_terminal(self.history[-1][0], True, -1, from_pos)
        await self.game_client.send_response(RESPONSE.SUCCESS, "img", {"payload": representation})

    async def show_blunder(self):
        if len(self.blunder_history) > 0:
            await self.game_client.send_response(RESPONSE.SUCCESS, "blunder", {"payload": self.blunder_history})
        else:
            await self.game_client.send_response(RESPONSE.SUCCESS, "No obvious blunder")

    async def timeline(self, start_index: int = -1, step: bool = False, unstep: bool = False):
        if start_index > -1:  # in case of initial timeline start
            self.timeline_start = start_index
        else:  # in case step / unstep
            start_index = self.timeline_start
        if step:
            start_index = self.timeline_start = self.timeline_start + 1
        elif unstep:
            start_index = self.timeline_start = self.timeline_start - 1
        if len(self.history) <= start_index or start_index < 0:
            await self.game_client.send_response(RESPONSE.ERROR, "Invalid index")
        else:
            await self.game_client.send_response(RESPONSE.SUCCESS, "Valid index")
            representation = self.game.draw_terminal(self.history[start_index][0], False, self.history[start_index][1])
            await self.game_client.send_response(RESPONSE.SUCCESS, "img", {"payload": representation})
            img1, img2 = self.game.draw(self.history[start_index][0], False, self.history[start_index][1])
            await self.game_client.send_image(img1, img2)
