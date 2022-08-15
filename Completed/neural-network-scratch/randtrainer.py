from main import *
import numpy as np


def training(iterations):
    # best network thus far
    lowest_loss = 9999999
    best_layer1_weights = layer1.weights.copy()
    best_layer1_biases = layer1.biases.copy()

    best_layer2_weights = layer2.weights.copy()
    best_layer2_biases = layer2.biases.copy()

    best_layer3_weights = layer3.weights.copy()
    best_layer3_biases = layer3.biases.copy()

    for iteration in range(iterations):
        layer1.weights += 0.05 * np.random.randn(2, 4)
        layer1.biases += 0.05 * np.random.randn(1, 4)
        layer2.weights += 0.05 * np.random.randn(4, 4)
        layer2.biases += 0.05 * np.random.randn(1, 4)
        layer3.weights += 0.05 * np.random.randn(4, 3)
        layer3.biases += 0.05 * np.random.randn(1, 3)

        layer1.process(X)
        activation1.process(layer1.output)

        layer2.process(activation1.output)
        activation2.process(layer2.output)

        layer3.process(activation2.output)
        softmax1.process(layer3.output)

        loss = loss_function.calculate(softmax1.output, y)
        predictions = np.argmax(softmax1.output, axis=1)
        accuracy = np.mean(predictions == y)

        if loss < lowest_loss:
            print("New set of weights found, iteration:", iteration, "loss:", loss, "acc:", accuracy)
            best_layer1_weights = layer1.weights.copy()
            best_layer1_biases = layer1.biases.copy()
            best_layer2_weights = layer2.weights.copy()
            best_layer2_biases = layer2.biases.copy()
            best_layer3_weights = layer3.weights.copy()
            best_layer3_biases = layer3.biases.copy()
            lowest_loss = loss
        else:
            layer1.weights = best_layer1_weights.copy()
            layer1.biases = best_layer1_biases.copy()
            layer2.weights = best_layer2_weights.copy()
            layer2.biases = best_layer2_biases.copy()
            layer3.weights = best_layer3_weights.copy()
            layer3.biases = best_layer3_biases.copy()
