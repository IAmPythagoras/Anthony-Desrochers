import torch
import torch.nn as nn
import torch.nn.functional as F


class NeuralNetwork(nn.Module):

    def __init__(self):
        super(NeuralNetwork, self).__init__()

        self.fc1 = nn.Linear(26, 40)
        self.fc2 = nn.Linear(40, 50)
        self.fc3 = nn.Linear(50,60)
        self.fc4 = nn.Linear(60,40)
        self.fc5 = nn.Linear(40, 18)#Final layer

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        x = torch.max(F.relu(self.fc5(x)))
        return x


net = NeuralNetwork()

print(net)