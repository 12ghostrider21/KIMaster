import logging
import asyncio
import time

from GameClient.player import Player
import numpy as np
from Tools.datatypes import EResponse
from tqdm import tqdm

log = logging.getLogger(__name__)


class Arena:
    """
    An Arena class where any 2 agents can be pit against each other.
    """

    def __init__(self, player1, player2, player3, game, game_client=None):
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
        self.player3 = player3  # nnet evaluating users moves (function: blunder)
        self.game = game
        self.game_client = game_client
        self.stop = False
        self.stop_lock = asyncio.Lock()
        self.history = []  # (board, curPlayer, iterator)
        self.blunder_history = []  # (iterator, action, curPlayer)
        self.timeline_start: int = 0

    def player_to_txt(self, curPlayer: int):
        match curPlayer:
            case 1:
                return "p1"
            case -1:
                return "p2"
            case _:
                return None

    async def send_response(self, response_code: EResponse, curPlayer: int | None, response_msg: str | None = None,
                            data: dict | None = None):
        await self.game_client.send_response(response_code,
                                             self.player_to_txt(curPlayer),
                                             response_msg,
                                             data)

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
                representation = self.game.draw_terminal(board, False, curPlayer)
                await self.send_response(EResponse.SUCCESS, None, "", {"board": representation})
                # img1 = self.game.draw(board, False, curPlayer)
                # img2 = self.game.draw(board, False, -curPlayer)
                # await self.game_client.send_image(img1, img2)
                await self.send_response(EResponse.SUCCESS, None, "Player" + str(curPlayer) + "'s turn:")
            if verbose:  # same as with blunder_history
                self.history.append((board, curPlayer, it))
            if not isinstance(players[curPlayer + 1], type(Player.play)):  # user (AI) is in charge to make a turn
                action = await players[curPlayer + 1](self.game.getCanonicalForm(board, curPlayer))  # the canonicalForm
                # of the board is the argument for the player function (lambda x : ... (x) / play(self,board))
                # players are at index 0 and 2 => curPlayer + 1 ==> -1 + 1 = 0; 1 + 1 = 2
                async with self.stop_lock:
                    if self.stop:
                        break
                if verbose:
                    # letting the own AI create a probability array for every action
                    ref_actions = self.player3(self.game.getCanonicalForm(board, curPlayer))

                    # sorting it and getting the worse half of all possible actions
                    sorted_list = sorted(ref_actions)  # sorted() is not overwriting the original ref_actions array
                    upper_half = len(sorted_list) // 2
                    bad_actions = sorted_list[:upper_half]

                    np_bad_actions = np.array(bad_actions)
                    np_ref_actions = np.array(ref_actions)

                    # getting the indices of the bad moves (the positions on the board (= move))
                    bad_actions = np.flatnonzero(np.isin(np_ref_actions, np_bad_actions))
                    for a in bad_actions:  # comparing move with rather bad moves for show_blunder function
                        if action == a:
                            self.blunder_history.append((it, action, curPlayer))
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

        if verbose:
            self.history.append((board, curPlayer, it))
            if not eval:
                representation = self.game.draw_terminal(board, False, curPlayer)
                await self.send_response(EResponse.SUCCESS, None, "", {"board": representation})
                # img1 = self.game.draw(board, False, curPlayer)
                # img2 = self.game.draw(board, False, -curPlayer)
                # await self.game_client.send_image(img1, img2)
        async with self.stop_lock:
            if self.stop:  # when giving up, stop_game is called as well => therefore (curPlayer * -1) is the winner
                self.stop = False
                if verbose and not eval:
                    await self.send_response(EResponse.SUCCESS, None, "Game over: ",
                                             {"turn": str(it), "result": curPlayer * -1})
                return curPlayer * -1
        if verbose and not eval:
            await self.send_response(EResponse.SUCCESS, None, "Game over: ",
                                     {"turn": str(it),
                                      "result": str(curPlayer * self.game.getGameEnded(board, curPlayer))})
        return curPlayer * self.game.getGameEnded(board, curPlayer)

    async def playGames(self, num, train=True):
        """
        Plays num games in which player1 starts num/2 games and player2 starts
        num/2 games.

        Returns:
            oneWon: games won by player1
            twoWon: games won by player2
            draws:  games won by nobody
        """

        half = int(num / 2)
        oneWon = 0
        twoWon = 0
        draws = 0
        for _ in tqdm(range(half), desc="Arena.playGames (1)"):
            gameResult = await self.playGame(verbose=False, eval=True)
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

        for i in tqdm(range(half), desc="Arena.playGames (2)"):
            if i == (half - 1) and not train:
                gameResult = await self.playGame(verbose=True, eval=True)
                async with self.stop_lock:
                    if self.stop:
                        self.stop = False
                        return oneWon, twoWon, draws
            else:
                gameResult = await self.playGame(verbose=False, eval=True)
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
        if not train:
            # eval is always against alphaZeroAI => the users AI is always player1 => curPlayer = 1
            await self.send_response(EResponse.SUCCESS, 1, "Evaluation finished",
                                     {"wins": oneWon,
                                      "losses": num - oneWon - draws,
                                      "draws": draws})

        return oneWon, twoWon, draws

    async def stop_game(self, flag: bool = True):
        async with self.stop_lock:
            self.stop = flag

    async def undo_move(self, amount: int):
        if len(self.history) >= 3:  # otherwise the user would try to undo a move he hasn't done yet
            for _ in range(amount * 2 + 1):  # amount * 2 because undoing enemies move as well; +1 because after the
                                                # loop, history gets appended once again
                self.history.pop()
                if len(self.history) == 1:  # if hand in amount is too high ==> going back to at least init_state of
                    # the board
                    break
        await self.stop_game()
        tmp = self.history[-1]
        self.history.pop()  # additional pop because the same state is added in play again when calling play
        asyncio.create_task(self.playGame(verbose=True, board=tmp[0], curPlayer=tmp[1], it=tmp[2]))
        await self.send_response(EResponse.SUCCESS, tmp[1], "Move successfully undone")

    async def draw_valid_moves(self, from_pos: int):
        # img = self.game.draw(self.game.getCanonicalForm(self.history[-1][0], -curPlayer), True, self.history[-1][1],
        #                      from_pos)
        # await self.game_client.send_image(img)
        try:
            representation = self.game.draw_terminal(self.history[-1][0], True, self.history[-1][1], from_pos)
            return representation
        except ValueError:
            return None

    async def show_blunder(self, player_pos: str) -> list:
        if player_pos == "p1":
            blunder_lst = [(iterator, action) for iterator, action, curPlayer in self.blunder_history if curPlayer == 1]
        else:
            blunder_lst = [(iterator, action) for iterator, action, curPlayer in self.blunder_history if
                           curPlayer == -1]
        return blunder_lst

    async def timeline(self, start_index: int = -1, step: bool = False, unstep: bool = False):
        if start_index > -1:  # in case of initial timeline start
            self.timeline_start = start_index
        else:  # in case step / unstep
            start_index = self.timeline_start
        if step:
            start_index = self.timeline_start + 1
        elif unstep:
            start_index = self.timeline_start - 1
        if len(self.history) <= start_index or start_index < 0:
            return None
        self.timeline_start = start_index
        representation = self.game.draw_terminal(self.history[start_index][0], False, self.history[start_index][1])
        return representation
        # img = self.game.draw(self.history[start_index][0], False, self.history[start_index][1])
        # await self.game_client.send_image(img)
