import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import random
from torch import optim
from Player import *


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class NeuralNetwork(nn.Module):

    def init(self):

        self.replay_memory_size = 10000
        self.initial_epsilon = 0.1
        self.final_epsilon = 0.0001
        self.minibatchsize = 32
        self.gamma = 0.99

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
exit()
criterion = nn.MSELoss()
replay_memory = []
epsilon = model.initial_epsilon
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

    state, reward, done, state_1 = env.step(action_index, ActionList)

    reward = torch.from_numpy(np.array([reward], dtype=np.float32)).unsqueeze(0)

    replay_memory.append((state, action_index, reward, state_1,done))

    if len(replay_memory) > model.replay_memory_size:
        replay_memory.pop(0)

    epsilon /= 1.1

    minibatch = random.sample(replay_memory, min( len(replay_memory), model.minibatch_size))

    state_batch = torch.cat(tuple(d[0] for d in minibatch)).to(device)
    action_batch = torch.cat(tuple(d[1] for d in minibatch)).to(device)
    reward_batch = torch.cat(tuple(d[2] for d in minibatch)).to(device)
    state_1_batch = torch.cat(tuple(d[3] for d in minibatch)).to(device)

    output_batch = model(state_batch)

    y_batch = torch.cat(tuple(reward_batch[i] if minibatch[i][4]
                              else reward_batch[i] + model.gamma * torch.max(output_batch[i])
                              for i in range(len(minibatch))))

    q_value = torch.sum(model(state_batch * action_batch, dim=1))

    optimizer.zero_grad()

    y_batch = y_batch.detach()

    loss = criterion(q_value, y_batch)

    loss.backward()
    optimizer.step()

    state = state_1


