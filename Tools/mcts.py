import logging
import math
import numpy as np

# Constants
EPS = 1e-8  # Small value to prevent division by zero errors
COEFFICIENT = 0.01  # Coefficient used for adjusting UCB values for sanctioned actions

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
        self.Es = {}  # Game end status for states
        self.Vs = {}  # Valid moves for states

        # Action tracking
        self.act = 0
        self.act_counter = 0
        self.sanctioned_acts = []  # List of sanctioned actions to avoid infinite loops

    def get_action_prob(self, canonical_board, temp=1):
        """
        Get the action probabilities for the given board state using MCTS.

        :param canonical_board: The current state of the board in its canonical form.
        :param temp: Temperature parameter for exploration. Lower values make the policy more deterministic.
        :return: A list of action probabilities.
        """
        # Perform MCTS simulations
        for i in range(self.args.numMCTSSims):
            self.search(canonical_board)

        # Get the string representation of the board
        s = self.game.stringRepresentation(canonical_board)
        # Get the visit counts for each action
        counts = [self.Nsa[(s, a)] if (s, a) in self.Nsa else 0 for a in range(self.game.getActionSize())]

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

    def search(self, canonical_board):
        """
        Perform a single MCTS search from the given board state.

        :param canonical_board: The current state of the board in its canonical form.
        :return: The negative value of the board state from the current player's perspective.
        """
        s = self.game.stringRepresentation(canonical_board)

        # Check if the game has ended for this state
        if s not in self.Es:
            self.Es[s] = self.game.getGameEnded(canonical_board, 1)
        if self.Es[s] != 0:
            return -self.Es[s]

        # If this state has not been visited before, it is a leaf node
        if s not in self.Ps:
            self.Ps[s], v = self.nnet.predict(canonical_board)
            valids = self.game.getValidMoves(canonical_board, 1)
            self.Ps[s] = self.Ps[s] * valids  # Mask invalid moves
            sum_ps_s = np.sum(self.Ps[s])
            if sum_ps_s > 0:
                self.Ps[s] /= sum_ps_s  # Renormalize
            else:
                log.error("All valid moves were masked, doing a workaround.")
                self.Ps[s] = self.Ps[s] + valids
                self.Ps[s] /= np.sum(self.Ps[s])

            self.Vs[s] = valids
            self.Ns[s] = 0
            return -v

        valids = self.Vs[s]
        cur_best = -float('inf')
        best_act = -1

        # Select action with highest upper confidence bound
        for a in range(self.game.getActionSize()):
            if valids[a]:
                if (s, a) in self.Qsa:
                    u = self.Qsa[(s, a)] + self.args.cpuct * self.Ps[s][a] * math.sqrt(self.Ns[s]) / (
                                1 + self.Nsa[(s, a)])
                    u += 1  # Make everything positive (negative u is possible)
                    if a in self.sanctioned_acts:
                        u *= COEFFICIENT
                else:
                    u = self.args.cpuct * self.Ps[s][a] * math.sqrt(self.Ns[s] + EPS)
                    u += 1
                    if a in self.sanctioned_acts:
                        u *= COEFFICIENT

                if u > cur_best:
                    cur_best = u
                    best_act = a

        a = best_act
        action = self.game.translate(canonical_board, 1, a)  # Translate index to actual move
        next_s, next_player = self.game.getNextState(canonical_board, 1, action)
        next_s = self.game.getCanonicalForm(next_s, next_player)

        if best_act == self.act:
            self.act_counter += 1
        else:
            self.act = best_act
            self.act_counter = 0

        if self.act_counter == 40 and not self.game.getGameEnded(next_s, 1):
            self.sanctioned_acts.append(best_act)

        v = self.search(next_s)

        if (s, a) in self.Qsa:
            self.Qsa[(s, a)] = (self.Nsa[(s, a)] * self.Qsa[(s, a)] + v) / (self.Nsa[(s, a)] + 1)
            self.Nsa[(s, a)] += 1
        else:
            self.Qsa[(s, a)] = v
            self.Nsa[(s, a)] = 1

        self.Ns[s] += 1
        return -v
