import sys

sys.path.append('..')

import torch
import torch.nn as nn
import torch.nn.functional as F


class NimNNet(nn.Module):
    def __init__(self, game, args):
        # game params
        self.board_size = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args

        super(NimNNet, self).__init__()
        self.fc1 = nn.Linear(self.board_size, args.num_channels)
        self.fc_bn1 = nn.BatchNorm1d(args.num_channels)

        self.fc2 = nn.Linear(args.num_channels, args.num_channels)
        self.fc_bn2 = nn.BatchNorm1d(args.num_channels)

        self.fc3 = nn.Linear(args.num_channels, self.action_size)

        self.fc4 = nn.Linear(args.num_channels, 1)

    def forward(self, s):
        s = s.view(-1, self.board_size)
        s = F.relu(self.fc_bn1(self.fc1(s)))
        s = F.relu(self.fc_bn2(self.fc2(s)))

        pi = self.fc3(s)
        v = self.fc4(s)

        return F.log_softmax(pi, dim=1), torch.tanh(v)
