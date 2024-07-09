import logging
import math
import numpy as np

# Constants
EPS = 1e-8  # Small value to prevent division by zero errors

# Setting up logging
log = logging.getLogger(__name__)


class MCTS:
    def __init__(self, game, nnet, args):
        """
        Initialize the MCTS (Monte Carlo Tree Search) object with the game, neural network, and arguments.

        :param game: The game object containing game-specific logic.
        :param nnet: The neural network used for predicting policy and value.
        :param args: Arguments containing various MCTS parameters.
        """
        self.game = game  # Game object
        self.nnet = nnet  # Neural network
        self.args = args  # Arguments for MCTS

        # Dictionaries to store MCTS values
        self.Qsa = {}  # Q values for state-action pairs
        self.Nsa = {}  # Visit count for state-action pairs
        self.Ns = {}  # Visit count for states
        self.Ps = {}  # Initial policy returned by the neural network

        # Game state storage
        self.Vs = {}  # Valid moves for states

        # Action tracking
        self.act = 0
        self.act_counter = 0
        self.sanctioned_acts = []  # List of sanctioned actions to avoid infinite loops

    def get_action_prob(self, board, cur_player, temp=1):
        """
        Get the action probabilities for the given board state using MCTS.

        :param board: The current state of the board in its canonical form.
        :param temp: Temperature parameter for exploration. Lower values make the policy more deterministic.
        :param cur_player: The player who is in turn.
        :return: A list of action probabilities.
        """
        # Perform MCTS simulations
        for i in range(self.args.numMCTSSims):
            self.search(board, cur_player)

        # Get the string representation of the board
        s = self.game.stringRepresentation(board)
        # Get the visit counts for each action
        counts = [self.Nsa[(s, cur_player, a)] if (s, cur_player, a) in self.Nsa else 0
                  for a in range(self.game.getActionSize())]

        if temp == 0:
            # Deterministic action selection
            best_as = np.array(np.argwhere(counts == np.max(counts))).flatten()
            best_a = np.random.choice(best_as)
            probs = [0] * len(counts)
            probs[best_a] = 1
            return probs

        # Apply temperature to visit counts
        counts = [x ** (1. / temp) for x in counts]
        counts_sum = float(sum(counts))
        probs = [x / counts_sum for x in counts]
        return probs

    def search(self, board, cur_player):
        """
        Perform a single MCTS search from the given board state.

        :param board: The current state of the board in its canonical form.
        :param cur_player: The current player.
        :return: The negative value of the board state from the current player's perspective.
        """
        s = self.game.stringRepresentation(board)

        # Check if the game has ended for this state
        status = self.game.getGameEnded(board, cur_player)
        if status != 0:
            return -status

        valids = self.game.getValidMoves(board, cur_player)
        self.Vs[(s, cur_player)] = valids

        # If this state has not been visited before, it is a leaf node
        if (s, cur_player) not in self.Ps:
            self.Ps[(s, cur_player)], v = self.nnet.predict(board)
            self.Ps[(s, cur_player)] = self.Ps[(s, cur_player)] * valids  # Mask invalid moves
            sum_ps_s = np.sum(self.Ps[(s, cur_player)])
            if sum_ps_s > 0:
                self.Ps[(s, cur_player)] /= sum_ps_s  # Renormalize
            else:
                log.error("All valid moves were masked, doing a workaround.")
                self.Ps[(s, cur_player)] = self.Ps[(s, cur_player)] + valids
                self.Ps[(s, cur_player)] /= np.sum(self.Ps[(s, cur_player)])

            self.Ns[(s, cur_player)] = 0
            return -v

        cur_best = -float('inf')
        best_act = -1

        # Select action with highest upper confidence bound
        for a in range(self.game.getActionSize()):
            if valids[a]:
                if (s, cur_player, a) in self.Qsa:
                    u = (self.Qsa[(s, cur_player, a)] + self.args.cpuct * self.Ps[(s, cur_player)][a] *
                         math.sqrt(self.Ns[(s, cur_player)]) / (1 + self.Nsa[(s, cur_player, a)]))
                else:
                    u = self.args.cpuct * self.Ps[(s, cur_player)][a] * math.sqrt(self.Ns[(s, cur_player)] + EPS)

                if u > cur_best:
                    cur_best = u
                    best_act = a

        a = best_act
        action = self.game.translate(board, cur_player, a)  # Translate index to actual move
        next_s, next_player = self.game.getNextState(board, cur_player, action)

        v = self.search(next_s, next_player)

        if (s, cur_player, a) in self.Qsa:
            self.Qsa[(s, cur_player, a)] = ((self.Nsa[(s, cur_player, a)] * self.Qsa[(s, cur_player, a)] + v) /
                                            (self.Nsa[(s, cur_player, a)] + 1))
            self.Nsa[(s, cur_player, a)] += 1
        else:
            self.Qsa[(s, cur_player, a)] = v
            self.Nsa[(s, cur_player, a)] = 1

        self.Ns[(s, cur_player)] += 1
        return -v
