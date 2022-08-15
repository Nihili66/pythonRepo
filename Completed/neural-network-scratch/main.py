from loss import *
from nnfs.datasets import *
from layer import *
from activation import *
from randtrainer import training

X, y = vertical_data(samples=100, classes=3)

# layer 1 of neurons
layer1 = Layer(2, 4)
activation1 = Activation_ReLU()

# layer 2 of neurons
layer2 = Layer(4, 4)
activation2 = Activation_ReLU()

# layer 3 of neurons
layer3 = Layer(4, 3)
softmax1 = Activation_Softmax()

# loss function
loss_function = Loss_CategoricalCrossentropy()

print(training(100000))
