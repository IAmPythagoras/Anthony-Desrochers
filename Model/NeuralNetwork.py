import torch
import torch.nn as nn
import torch.nn.functional as F

import random
from torch import optim
from Player import *


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class NeuralNetwork(nn.Module):

    def init(self):


        self.initial_epsilon = 0.1
        self.final_epsilon = 0.0001

        super(NeuralNetwork, self).init()

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
        x = self.fc5(x)
        return x


character = BlackMage(2.19, [], [])
env = Fight(character) #Initiate environment
state = character.getState()
model = NeuralNetwork()

optimizer = optim.Adam(model.parameters(), lr=1e-6)
criterion = nn.MSELoss()

#print(net)

ActionList = torch.zero_(0)
for iteration in range(10):

    #get output from neural network
    output = model(state).to(device)

    #Will do action (either random one, or the one predicted by the model)

    random_action = random.random() <= model.epsilon

    action_index = [torch.randint(17, torch.Size([]), dtype=torch.int)
                        if random_action
                        else torch.argmax(output)][0].to(device)

    ActionList = torch.cat((ActionList, action_index))
    #get nextstate and reward and info

    state, reward, done = env.step(action_index, ActionList)
