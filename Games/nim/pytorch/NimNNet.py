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
        self.fc1 = nn.Linear(self.board_size, 1024)
        self.fc_bn1 = nn.BatchNorm1d(1024)

        self.fc2 = nn.Linear(1024, 512)
        self.fc_bn2 = nn.BatchNorm1d(512)

        self.fc3 = nn.Linear(512, self.action_size)

        self.fc4 = nn.Linear(512, 1)

    def forward(self, s):
        # s: batch_size x board_size
        s = s.view(-1, self.board_size)
        s = F.relu(self.fc_bn1(self.fc1(s)))  # batch_size x 1024
        s = F.dropout(s, p=self.args.dropout, training=self.training)
        s = F.relu(self.fc_bn2(self.fc2(s)))  # batch_size x 512
        s = F.dropout(s, p=self.args.dropout, training=self.training)

        pi = self.fc3(s)  # batch_size x action_size
        v = self.fc4(s)  # batch_size x 1

        return F.log_softmax(pi, dim=1), torch.tanh(v)
