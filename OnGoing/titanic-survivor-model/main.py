import torch
import torch.nn as nn # All neural network modules, nn.Linear, nn.Conv2d, BatchNorm, Loss functions
import torch.optim as optim # For all Optimization algorithms, SGD, Adam, etc.
import torch.nn.functional as F # All functions that don't have any parameters
from torch.utils.data import DataLoader # Gives easier dataset management and creates mini batches
import numpy as np
import pandas as pd
from dataset import CustomTrainSet

# Network class
class NN(nn.Module):
    def __init__(self, input_size, output_size):
        super(NN, self).__init__()
        self.layer1 = nn.Linear(input_size, 4)
        self.layer2 = nn.Linear(4, output_size)

    def forward(self, x):
        O1 = self.layer1(x)
        O1F = F.relu(O1)
        O2 = self.layer2(O1F)
        O2F = F.softmax(O2, dim=1)
        return O2F


# settings
input_size = 5
output_size = 1
batch_size = 64
learning_rate = 0.01
num_epochs = 1

# data sets
train = pd.read_csv("train.csv")
# get the parameter values and survivorship
train_survived = np.asarray(train.iloc[:, 0])
train_param = np.asarray(train.iloc[:, 1:])
param = torch.from_numpy(train_param).float()
survived = torch.from_numpy(train_survived).float()

# data loarder
train_data = CustomTrainSet(param, survived)
trainloader = DataLoader(train_data, batch_size=batch_size, shuffle=True)

# initializing the network
device = torch.device("cpu")
model = NN(input_size, output_size).to(device)

# loss
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# training loop
def training(model, trainloader):
    for epoch in range(10):  # no. of epochs
        running_loss = 0
        for data in trainloader:
            # parametrs and survived to GPU if available
            inputs, survived = data[0].to(device, non_blocking=True), data[1].to(device, non_blocking=True)
            # set the parameter gradients to zero
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, survived)
            # propagate the loss backward
            loss.backward()
            # update the gradients
            optimizer.step()

            running_loss += loss.item()
        print('[Epoch %d] loss: %.3f' %
              (epoch + 1, running_loss / len(trainloader)))

    print('Done Training')


training(model, trainloader)
