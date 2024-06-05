import numpy as np
from tqdm import tqdm

from player import Player
from Tools.Response import *
from Tools.game_states import GAMESTATE


class Arena:
    """
    An Arena class where any 2 agents can be pit against each other.
    """

    def __init__(self, player1, player2, evaluator, game, game_client=None):
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
        self.evaluator = evaluator  # nnet evaluating users moves (function: blunder)
        self.game = game
        self.game_client = game_client
        self.history = []  # (board, cur_player, iterator)
        self.blunder_history = []  # (iterator, action, curPlayer)
        self.timeline_start: int = 0
        self.swapped = False

    async def send_response(self, response_code: R_CODE, cur_player: int | None, data: dict = None):
        await self.game_client.send_response(code=response_code,
                                             p_pos=self.player_to_txt(cur_player),
                                             data=data)

    # an episode = 1 Game played
    async def playGame(self, verbose=False, eval=False, board=None, cur_player: int = 1, it: int = 0):
        """
        Executes one episode of a game.

        Returns:
            either
                winner: player who won the game (1 if player1, -1 if player2)
            or
                draw result returned from the game that is neither 1, -1, nor 0.
        """
        players = [self.player2, None, self.player1]  # player2 and player1 are functions
        if board is None:
            board = self.game.getInitBoard()

        while self.game.getGameEnded(board, cur_player) == 0:  # 0 if game is not finished
            if verbose or eval:
                await self.send_board(board, cur_player)
                if verbose:
                    self.history.append((board, cur_player, it))
                    if not eval:
                        await self.send_board_representation(board, cur_player)

            # user / userAI in turn
            if not isinstance(players[cur_player + 1], type(Player.play)):
                action = await players[cur_player + 1](self.game.getCanonicalForm(board, cur_player))
                if action is None:
                    return None
                #if verbose:
                #    self.evaluate_blunder(action)

            # websiteAI in turn
            else:
                action = np.argmax(players[cur_player + 1](self.game.getCanonicalForm(board, cur_player)))

            valids = self.game.getValidMoves(self.game.getCanonicalForm(board, cur_player), 1)
            if valids[action] == 0:
                assert valids[action] > 0

            board, cur_player = self.game.getNextState(board, cur_player, action)
            it += 1

        if verbose:
            self.history.append((board, cur_player, it))
            if verbose and not eval:
                await self.send_board_representation(board, cur_player)
                await self.send_response(R_CODE.P_GAMEOVER, None,
                                         {"result": round(cur_player * self.game.getGameEnded(board, cur_player)),
                                          "turn": it})
                self.game_client.state = GAMESTATE.FINISHED
        return round(cur_player * self.game.getGameEnded(board, cur_player))

    async def playGames(self, num, train=True):
        """
        Plays num games in which player1 starts num/2 games and player2 starts
        num/2 games.

        Returns:
            one_won: games won by player1
            two_won: games won by player2
            draws:  games won by nobody
        """

        half = int(num / 2)
        one_won = 0
        two_won = 0
        draws = 0

        for i in [1, 2]:
            break_outer = False
            for j in tqdm(range(half), desc=f"Arena.playGames ({i})"):
                if train:
                    game_result = await self.playGame(verbose=False, eval=False)
                elif i == 1 and j == 0:  # in order to track blunder and timeline for at least 1 game of the evaluation
                    game_result = await self.playGame(verbose=True, eval=True)
                else:
                    game_result = await self.playGame(verbose=False, eval=True)
                if game_result is None:
                    if i == 1:
                        break_outer = True
                        break
                    break
                if game_result == 1:
                    one_won += 1
                elif game_result == -1:
                    two_won += 1
                else:
                    draws += 1
            if break_outer:
                break
            self.player1, self.player2 = self.player2, self.player1
            self.swapped = True if not self.swapped else False
            tmp = one_won
            one_won = two_won
            two_won = tmp

        if not train:
            # eval is always against alphaZeroAI => the users AI is always player1 => curPlayer = 1
            await self.send_response(R_CODE.P_EVALOVER, 1, {"wins": one_won,
                                                            "losses": two_won,
                                                            "draws": draws})
        self.game_client.state = GAMESTATE.FINISHED
        return one_won, two_won, draws

    def evaluate_blunder(self, action):
        board = self.history[-1][0]
        cur_player = self.history[-1][1]
        it = self.history[-1][2]
        # letting the websiteAI create a probability array for every action
        ref_actions = self.evaluator(self.game.getCanonicalForm(board, cur_player))

        # sorting it and getting the worse half of all possible actions
        sorted_list = sorted(ref_actions)
        filtered_list = [action for action in sorted_list if action != 0]
        upper_half = len(filtered_list) // 2
        bad_actions = filtered_list[:upper_half]

        # getting the indices of the bad moves (the positions on the board (= move))
        bad_actions = np.flatnonzero(np.isin(np.array(ref_actions), np.array(bad_actions)))
        for a in bad_actions:  # comparing move with rather bad moves for show_blunder function
            if action == a:
                self.blunder_history.append((it, action, cur_player))

    async def send_board(self, board: np.array, cur_player: int):
        await self.send_response(R_CODE.P_BOARD, cur_player, {"board": board.tolist()})

    async def send_board_representation(self, board: np.array, cur_player: int):
        representation = self.game.draw_terminal(board, False, cur_player)
        await self.send_response(R_CODE.P_REPRESENTATION, None, {"representation": representation})
        img1 = self.game.draw(board, False, cur_player)
        img2 = self.game.draw(board, False, -cur_player)
        await self.game_client.broadcast_image(img1, img2)

    def player_to_txt(self, cur_player: int) -> str | None:
        if self.swapped:
            cur_player = -cur_player
        match cur_player:
            case 1:
                return "p1"
            case -1:
                return "p2"
            case _:
                return None

    async def undo_move(self, amount: int) -> Response:
        if len(self.history) >= 3:  # otherwise the user would try to undo a move he hasn't done yet
            final_amount = amount * 2  # amount * 2 because undoing enemies move as well
            if self.game_client.pit.arena_task.done() and self.history[-1][1] == -1:  # if game is finished, special
                # rules are applied (subtract 1 when being the winner (user/userAI) in order to have correct logic)
                final_amount -= 1
            for _ in range(final_amount):
                self.history.pop()
                if len(self.history) == 1:  # if hand in amount is too high ==> going back to at least init_state of
                    # the board
                    break
        it = self.history[-1][2]
        self.blunder_history = [self.blunder_history[i] for i in range(len(self.blunder_history))
                                if self.blunder_history[i][0] < it]
        tmp = self.history[-1]
        self.history.pop()  # additional pop because the same state is added again at the beginning of play
        await self.game_client.pit.start_game(num_games=1, verbose=True, board=tmp[0], cur_player=tmp[1], it=tmp[2])
        return Response(R_CODE.P_VALIDUNDO)

    async def draw_valid_moves(self, from_pos: int):
        try:
            img = self.game.draw(self.game.getCanonicalForm(self.history[-1][0], self.history[-1][1]), True,
                                 self.history[-1][1], from_pos)
            representation = self.game.draw_terminal(self.history[-1][0], True, self.history[-1][1], from_pos)
            return img, representation
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
        img = self.game.draw(self.history[start_index][0], False, self.history[start_index][1])
        representation = self.game.draw_terminal(self.history[start_index][0], False, self.history[start_index][1])
        return img, representation
