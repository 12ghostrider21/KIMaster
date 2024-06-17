import math
import numpy as np

EPS = 1e-8


# MCTS resulting in a tree with nodes having v value, Qsa and so on determined => knowing which child node to choose
# (which action (=move )) based on neural net (probabilities (policy vector), v value)

class MCTS:
    """
    This class handles the MCTS tree.
    s is the state, a is the action (the move to be made)
    #times is the count

    """

    def __init__(self, game, nnet, args):
        self.game = game
        self.nnet = nnet
        self.args = args
        self.Qsa = {}  # stores Q values for s,a (as defined in the paper) Q Value is the value of how good an action is
        # called ucd score in YT Video for alpha zero ==> min 21:30
        # child nodes / actions with the highest ucd score are getting chosen for next iteration of MCTS
        self.Nsa = {}  # stores #times edge s,a was visited
        self.Ns = {}  # stores #times board s was visited
        self.Ps = {}  # stores initial policy (returned by neural net)

        self.Es = {}  # stores game.getGameEnded ended for board s
        self.Vs = {}  # stores game.getValidMoves for board s

        # ... = {}   => key-value maps (for each state values)

    def getActionProb(self, canonicalBoard, temp=1):
        """
        This function performs numMCTSSims simulations of MCTS starting from
        canonicalBoard.

        Returns:
            probs: a policy vector where the probability of the ith action is
                   proportional to Nsa[(s,a)]**(1./temp)       # syntax 1. => 1 gets interpreted as float
             # policy vector is an array with probability distribution for each action (move)
             # temp is C in the video for alpha zero on YT => its a value determining whether to focus on exploration or
             # exploitation
        """
        for i in range(self.args.numMCTSSims):
            self.search(canonicalBoard)

        s = self.game.stringRepresentation(canonicalBoard)
        counts = [self.Nsa[(s, a)] if (s, a) in self.Nsa else 0 for a in
                  range(self.game.getActionSize())]  # in a list for every
        # action (move) having the count saved into a list or otherwise 0 is added
        # s = state of the game (node/ board)
        # letzten Endes: bei mehreren MCTS-Simulationsdurchgängen (numMCTSSims), welche Kanten dort
        # eben am häufigsten abgelaufen wurden ==> tendentiell die besten actions dann

        if temp == 0:  # has something to do with exploration and exploitation (rather exploit more here if temp = 0)
            bestAs = np.array(np.argwhere(counts == np.max(counts))).flatten()
            bestA = np.random.choice(bestAs)
            probs = [0] * len(counts)  # len(counts) = at TTT its 9 + 1 => 9 possible actions => [0,0,0,0,0,0,0,0,0,0]
            probs[bestA] = 1  # e.g. [0,0,0,0,1,0,0,0,0]
            return probs

        # else (exploration (temp = 1))
        counts = [x ** (1. / temp) for x in counts]
        counts_sum = float(sum(counts))
        probs = [x / counts_sum for x in
                 counts]  # [0.1, 0.2, 0.25, 0.05, 0.05, 0.1, 0.05, 0.05, 0.05, 0]; last one=flag
        return probs

    def search(self, canonicalBoard):
        """
        This function performs one iteration of MCTS. It is recursively called
        till a leaf node is found. The action chosen at each node is one that
        has the maximum upper confidence bound as in the paper.

        Once a leaf node is found, the neural network is called to return an
        initial policy P and a value v for the state. This value is propagated
        up the search path. In case the leaf node is a terminal state, the
        outcome is propagated up the search path. The values of Ns, Nsa, Qsa are
        updated.

        NOTE: the return values are the negative of the value of the current
        state. This is done since v is in [-1,1] and if v is the value of a
        state for the current player, then its value is -v for the other player.

        # Note by Max
        # -1 would be the worst value for the enemy in its state => and in the MCTS we are 1 turn ahead of our owns, so
        # we choose the action with the lowest value in order to have the best outcome for ourselves

        # to understand the (alpha) MCTS => freecodecamp video for alpha zero on YT (min 31)
        # the neural net called on the individual parent node of the child nodes delivers the policy vector for the
        # child nodes (a probability for each child (all probabilities in sum =1)) as well as the v value
        # (probability between -1 and 1) for the state (the parent node of the child nodes)
        # => the child node with the highest probability is getting chosen (would be also the node with the highest
        # ucd score (here "Qsa" called))
        # => v getting set for the parent node and getting back propagated all the way up to the root node (added to the
        current value)
        # difference between MCTS and alphaMCTS => no longer simulating every explored node til the end (game ended) but
        # valuing a node just by the result of the neural net for the child node


        Returns:
            v: the negative of the value of the current canonicalBoard
        """

        s = self.game.stringRepresentation(
            canonicalBoard)  # s is the state (the node in the MCTS, the board (positions))

        if s not in self.Es:  # Es stores for every board state (node) whether game is ended (and who has won) or not
            self.Es[s] = self.game.getGameEnded(canonicalBoard,
                                                1)  # if not ended (most cases), a 0 will be written for that state s
        if self.Es[s] != 0:  # means game ended
            # terminal node
            return -self.Es[s]  # 1 or -1

        if s not in self.Ps:  # if no policy already calculated for that state (board position) = leaf node
            # leaf node
            self.Ps[s], v = self.nnet.predict(canonicalBoard)  # exactly what described in the function doc above happens
            # policy vector for the child nodes (states) of that node (state)
            # and v value for that node is calculated
            valids = self.game.getValidMoves(canonicalBoard,
                                             1)  # btw: its always player 1, because the board gets unified
            # (=canonical board)
            self.Ps[s] = self.Ps[s] * valids  # masking invalid moves => invalid moves are 0, valid moves are 1
            sum_Ps_s = np.sum(self.Ps[s])
            if sum_Ps_s > 0:
                self.Ps[s] /= sum_Ps_s  # renormalize because the sum of the probabilities is no longer 1, but lower,
            else:
                # if it is 0, all valid moves being masked (0 <= sum_Ps_s <= 1) => 1 =all moves valid, 0 =0 moves valid
                # because the sum of all probabilities is 1 when all moves are valid (=1) =>
                # "self.Ps[s] = self.Ps[s] * valids"

                # but 0 cannot be (0 moves valid), because then game would be game over =>
                # and game over is treated few lines above this resulting in a return statement  => so there MUST be
                # valid moves ==> but those are being masked because the probability was zero for that move
                # ==> most likely an error in the neural net calculating the policy vector with the probability
                # distribution

                # if all valid moves were masked make all valid moves equally probable => its line
                # "self.Ps[s] = self.Ps[s] + valids" ==> so the probability for each of those are 1 then (equally
                # probable) => in sum more than 1 => therefore that line "self.Ps[s] /= np.sum(self.Ps[s])"

                # NB! All valid moves may be masked if either your NNet architecture is insufficient or you've get
                # overfitting or something else. If you have got dozens or hundreds of these messages you should pay
                # attention to your NNet and/or training process.
                self.Ps[s] = self.Ps[s] + valids
                self.Ps[s] /= np.sum(self.Ps[s])  # normalizing them, therefore the sum over all probabilities is 1
                # afterwards again

            self.Vs[s] = valids  # Vs stores valid moves for the given state (node/ board)
            self.Ns[s] = 0  # stores times the state got visited (0 because it's the first time getting visited, no
            # revisits so far)
            return -v

        # following code if s is in Ps (policy vector already calculated) and therefore Vs as well:

        valids = self.Vs[s]
        cur_best = -float('inf')
        best_act = -1  # best action

        # pick the action with the highest upper confidence bound
        for a in range(self.game.getActionSize()):  # with TicTacToe getActionSize() is amount of fields (9) + 1
            if valids[a]:  # just True if it is a valid move (1)
                if (s, a) in self.Qsa:
                    u = self.Qsa[(s, a)] + self.args.cpuct * self.Ps[s][a] * math.sqrt(self.Ns[s]) / (  # thats kind of
                            1 + self.Nsa[(s, a)])  # the formula in the YT video was applied to calc the ucd score (Qsa)
                else:
                    u = self.args.cpuct * self.Ps[s][a] * math.sqrt(self.Ns[s] + EPS)  # Q = 0 ? ; Max: here as well
                    # kind of
                if u > cur_best:
                    cur_best = u
                    best_act = a

        a = best_act
        next_s, next_player = self.game.getNextState(canonicalBoard, 1, a)
        next_s = self.game.getCanonicalForm(next_s, next_player)

        v = self.search(next_s)  # recursively going through the MCT => always -v as return value
        # so -v is being back propagated through recursion (and all the other values Qsa ...
        # being set as well)

        if (s, a) in self.Qsa:  # 2nd or more times that this node is revisited
            self.Qsa[(s, a)] = (self.Nsa[(s, a)] * self.Qsa[(s, a)] + v) / (self.Nsa[(s, a)] + 1)
            self.Nsa[(s, a)] += 1

        else:  # first time this node is revisited, otherwise Qsa would be set
            self.Qsa[(s, a)] = v
            self.Nsa[(s, a)] = 1

        self.Ns[s] += 1
        return -v

# MCTS resulting in a tree with nodes having v value, Qsa and so on determined => knowing which child node to choose
# (which action (=move )) based on neural net (probabilities (policy vector), v value)
