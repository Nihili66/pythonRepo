import numpy as np

class Activation_ReLU:
    def process(self, inputs):
        self.output = np.maximum(0, inputs)

class Activation_Softmax:
    def process(self, inputs):
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        self.output = probabilities
