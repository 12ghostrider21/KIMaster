import os
import time
import numpy as np
import sys
sys.path.append('../../')
import pandas as pd
import torch
import torch.optim as optim
from torch.autograd import Variable

from Games.go.pytorch.GoAlphaNet import AlphaNetMaker as NetMaker
from Games.go.pytorch.GoNNet import GoNNet

from Tools.utils import *
from Tools.neural_net import NeuralNet

args = dotdict({
    'lr': 0.001,
    'dropout': 0.3,
    'epochs': 5,
    'batch_size': 64,
    'cuda': torch.cuda.is_available(),
    'num_channels': 512,
})

print(args)


class NNetWrapper(NeuralNet):
    def __init__(self, game,t='RES'):
        self.netType=t
        if t=='RES':
        # self.nnet = onnet(game, args)
            netMkr=NetMaker(game,args)
            self.nnet=netMkr.makeNet()
        else:
            self.nnet=GoNNet(game,args)
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()

        if args.cuda:
            self.nnet.cuda()

    def train(self, examples):
        """
        examples: list of examples, each example is of form (board, pi, v)
        """
        optimizer = optim.Adam(self.nnet.parameters())
        trainLog={
            'EPOCH':[],
            'P_LOSS':[],
            'V_LOSS':[]
        }

        for epoch in range(args.epochs):
            print('EPOCH ::: ' + str(epoch+1))
            trainLog['EPOCH'].append(epoch)
            self.nnet.train()
            data_time = AverageMeter()
            batch_time = AverageMeter()
            pi_losses = AverageMeter()
            v_losses = AverageMeter()
            end = time.time()

            max=int(len(examples)/args.batch_size)
            batch_idx = 0

            while batch_idx < int(len(examples)/args.batch_size):
                sample_ids = np.random.randint(len(examples), size=args.batch_size)
                boards, pis, vs = list(zip(*[examples[i] for i in sample_ids]))
                boards = torch.FloatTensor(np.array(boards).astype(np.float64))
                target_pis = torch.FloatTensor(np.array(pis))
                target_vs = torch.FloatTensor(np.array(vs).astype(np.float64))

                # predict
                if args.cuda:
                    boards, target_pis, target_vs = boards.contiguous().cuda(), target_pis.contiguous().cuda(), target_vs.contiguous().cuda()
                boards, target_pis, target_vs = Variable(boards), Variable(target_pis), Variable(target_vs)

                # measure data loading time
                data_time.update(time.time() - end)
                # print(boards.shape)
                # compute output
                out_pi, out_v = self.nnet(boards)
                # print(out_pi,target_pis)
                # print(out_v,target_vs)

                l_pi = self.loss_pi(target_pis, out_pi)
                l_v = self.loss_v(target_vs, out_v)
                total_loss = l_pi + l_v

                # record loss
                pi_losses.update(l_pi.data[0], boards.size(0))
                v_losses.update(l_v.data[0], boards.size(0))

                # compute gradient and do SGD step
                optimizer.zero_grad()
                total_loss.backward()
                optimizer.step()

                # measure elapsed time
                batch_time.update(time.time() - end)
                end = time.time()

                batch_idx += 1

            trainLog['P_LOSS'].append(pi_losses.avg)
            trainLog['V_LOSS'].append(v_losses.avg)

        return pd.DataFrame(data=trainLog)


    def predict(self, board):
        """
        board: np array with board
        """
        # timing
        start = time.time()

        # preparing input
        board = torch.FloatTensor(board.astype(np.float64))
        if args.cuda: board = board.contiguous().cuda()
        # print(board)
        board = Variable(board,requires_grad=False)
        board = board.view(1, self.board_x, self.board_y)

        self.nnet.eval()

        pi, v = self.nnet(board)

        # print('PREDICTION TIME TAKEN : {0:03f}'.format(time.time()-start))
        return torch.exp(pi).data.cpu().numpy()[0], v.data.cpu().numpy()[0]

    def loss_pi(self, targets, outputs):

        return -torch.sum(targets*outputs)/targets.size()[0]

    def loss_v(self, targets, outputs):
        return torch.sum((targets-outputs.view(-1))**2)/targets.size()[0]

    def save_checkpoint(self, folder='R_checkpoint', filename='R_checkpoint.pth.tar'):
        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print("Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        torch.save({
            'state_dict' : self.nnet.state_dict(),
        }, filepath)

    def load_checkpoint(self, folder='R_checkpoint', filename='R_checkpoint.pth.tar'):
        # https://github.com/pytorch/examples/blob/master/imagenet/main.py#L98
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            raise BaseException("No model in path {}".format(filepath))
        checkpoint = torch.load(filepath)
        self.nnet.load_state_dict(checkpoint['state_dict'])
