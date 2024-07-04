import numpy as np
import torch.utils.model_zoo as model_zoo
import torch
import torchvision as tv
import torch.nn as nn
from torch.nn.functional import Variable
from scipy import misc
import math
import torch.nn.functional as F

from torchvision.models.densenet import DenseNet
from torchvision.models.resnet import BasicBlock
from torchvision.models.resnet import Bottleneck

class DenseGoNet(DenseNet):
    def __init__(self):
        pass
    def forward(self, x):
        pass
