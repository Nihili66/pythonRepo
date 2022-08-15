from loss import *
from nnfs.datasets import *
from layer import *
from activation import *
from randtrainer import training

np.random.seed(0)

class OneHiddenLayerNetwork:

    @staticmethod
    def tang(y):
        return np.tanh(y)

    @staticmethod
    def derivative_tang(y):
        return 1.0 - y ** 2

    @staticmethod
    def sigmoid(y):
        return 1 / (1 + np.exp(-y))

    @staticmethod
    def derivative_sigmoid(y):
        return y * (1 - y)

    def __init__(self, learning_rate=0.1):
        self.learning_rate = learning_rate
        self.output = None
        # weights with random values
        self.weights = [
            np.random.uniform(low=-0.2, high=0.2, size=(2, 4)),
            np.random.uniform(low=-2, high=2, size=(4, 4)),
            np.random.uniform(low=-2, high=2, size=(4, 3))
        ]
        # layer 1 of neurons
        self.layer1 = Layer(2, 4)
        self.activation1 = Activation_ReLU()
        # layer 2 of neurons
        self.layer2 = Layer(4, 4)
        self.activation2 = Activation_ReLU()
        # layer 3 of neurons
        self.layer3 = Layer(4, 3)
        self.softmax1 = Activation_Softmax()
        # loss function
        self.loss_function = Loss_CategoricalCrossentropy()

    def derivative_activation(self, activation_type, y):
        if activation_type == 'sigmoid':
            return self.derivative_sigmoid(y)
        if activation_type == 'tang':
            return self.derivative_tang(y)

        raise ValueError('Undefined derivative activation function: {}'.format(activation_type))

    #
    # forward pass
    # layer by layer
    #
    def feed_forward_pass(self, x_values):

        # forward
        self.layer1.process(x_values)
        self.activation1.process(self.layer1.output)

        self.layer2.process(self.activation1.output)
        self.activation2.process(self.layer2.output)

        self.layer3.process(self.activation2.output)
        self.softmax1.process(self.layer3.output)

        # last layer is an output
        return self.softmax1.output

    #
    # back propagation error through the network layers
    #
    def backward_pass(self, target_output, actual_output):

        # divergence of network output
        err = (target_output - actual_output)

        # backward from output to input layer
        # propagate gradients using chain rule
        for backward in range(2, 0, -1):
            err_delta = err * self.derivative_activation('tang', self.layers[backward])

            # update weights using computed gradient
            self.weights[backward - 1] += self.learning_rate * np.dot(self.layers[backward - 1].T, err_delta)

            # propagate error using updated weights of previous layer
            err = np.dot(err_delta, self.weights[backward - 1].T)

    def train(self, x_values, target):
        self.output = self.feed_forward_pass(x_values)
        self.backward_pass(target, self.output)

    def predict(self, x_values):
        return self.feed_forward_pass(x_values)


#
# X - XOR dataset data
# y = target
#
X = np.array(([0, 0], [0, 1], [1, 0], [1, 1]), dtype=float)
y = np.array(([0], [1], [1], [0]), dtype=float)

network = OneHiddenLayerNetwork(learning_rate=0.1)
iterations = 100000

# training
for i in range(iterations):
    network.train(X, y)

    ten = iterations // 10
    if i % ten == 0:
        print('-' * 10)
        print("Iteration number: " + str(i) + ' / ' +
              "Squared loss: " + str(np.mean(np.square(y - network.output))))

# predict
for i in range(len(X)):
    print('-' * 10)
    print('Input value: ' + str(X[i]))
    print('Predicted target: ' + str(network.predict(X[i])))
    print('Actual target: ' + str(y[i]))