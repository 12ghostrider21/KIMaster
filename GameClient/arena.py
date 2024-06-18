import numpy as np

from Tools.rcode import RCODE


class Arena:
    def __init__(self, game_client):
        self.game_client = game_client
        self.game = None
        self.game_name: str = ""
        self.history: list = []  # [board, cur_player, iteration]

        self.player1 = None
        self.player2 = None
        self.cur_player = None
        self.stop: bool = False

    def set_arena(self, game, game_name, play1, play2):
        self.game = game
        self.game_name = game_name
        self.player1 = play1
        self.player2 = play2
        self.history.clear()

    def undo_move(self, amount: int) -> tuple[np.array, int, int]:
        if len(self.history) >= 3:  # otherwise the user would try to undo a move he hasn't done yet
            final_amount = amount * 2  # amount * 2 because undoing enemies move as well
            if self.game_client.pit.arena_task is None and self.history[-1][1] == -1:  # if game is finished, special
                # rules are applied (subtract 1 when being the winner (user/userAI) in order to have correct logic)
                final_amount -= 1
            for _ in range(final_amount):
                self.history.pop()
                if len(self.history) == 1:  # if hand in amount is too high ==> going back to at least init_state of
                    # the board
                    break
        it = self.history[-1][2]
        tmp = self.history[-1]
        self.history.pop()  # additional pop because the same state is added again at the beginning of play
        return tmp[0], tmp[1], tmp[2]

    def get_last_board(self) -> list:
        if len(self.history) > 0:
            return self.history[-1]
        return [self.game.getInitBoard(), 1, 0]

    async def playGame(self, board=None, cur_player: int = 1, it: int = 0):
        if board is None:
            board = self.game.getInitBoard()
        players = [self.player2, None, self.player1]
        while self.game.getGameEnded(board, cur_player) == 0 and not self.stop:  # 0 if game is not finished
            self.cur_player = cur_player
            self.history.append([board, cur_player, it])
            await self.game_client.broadcast_board(board, cur_player, self.game_name, False)

            p = players[cur_player + 1]
            canonical_board = self.game.getCanonicalForm(board, cur_player)
            valids = self.game.getValidMoves(canonical_board, 1)
            to = "p1" if cur_player == 1 else "p2"
            action = None
            while not self.stop:
                action = p()
                if action is None:
                    continue
                if isinstance(action, bool):  # do a request to server with ai move
                    await self.game_client.send_cmd(command="ai_move", command_key=self.game_name, p_pos=to,
                                                    data={"board": board.tolist(),
                                                          "cur_player": cur_player,
                                                          "dtype": str(board.dtype),
                                                          "shape": board.shape,
                                                          "it": it,
                                                          "key": self.game_client.key})
                    continue

                if action >= len(valids):
                    await self.game_client.send_response(code=RCODE.P_INVALIDMOVE, to=to)
                    continue
                if valids[action]:
                    print(f"Valid ACTION of: {to}", action)
                    break
                await self.game_client.send_response(code=RCODE.P_INVALIDMOVE, to=to)
            if not self.stop:
                board, cur_player = self.game.getNextState(board, cur_player, action)
                it += 1

        if not self.stop:
            await self.game_client.broadcast_board(board, cur_player, self.game_name, False)
            await self.game_client.send_response(RCODE.P_GAMEOVER, None,
                                                 {"result": round(
                                                     cur_player * self.game.getGameEnded(board, cur_player)),
                                                  "turn": it})
        self.game_client.pit.arena_task = None  # deactivate task
