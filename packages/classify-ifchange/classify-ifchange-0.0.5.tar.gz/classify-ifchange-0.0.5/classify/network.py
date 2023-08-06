import torch
from torch.nn import Linear, Dropout, Module, ReLU


class SimpleClassifier(Module):
    def __init__(self, n_class, dim=512, dropout=0.3):
        super(SimpleClassifier, self).__init__()
        self.dim = dim
        self.dropout = Dropout(dropout)
        self.fc = Linear(dim//2, n_class)
        self.hidden = Linear(dim, dim//2)
        self.selu = ReLU()


    def forward(self, x):
        x = self.selu(self.hidden(x))
        x = self.dropout(self.fc(x))
        return x
