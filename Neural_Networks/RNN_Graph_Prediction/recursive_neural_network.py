import numpy as np
import matplotlib.pyplot as plt

import csv
import math
from typing import List, Tuple
import time


class ActivationFunction:
    def __init__(self, activation_function: callable, activation_derivative: callable):
        self.activation_function = activation_function
        self.activation_derivative = activation_derivative


class RecursiveNeuralNetwork:
    def __init__(
        self, input_size: int, activation_function: ActivationFunction, seed: int = 0
    ):
        """A simple 1 layer recurent neural network

        Args:
            input_size (int): The size of the input / output / hidden layer
            activation_function (ActivationFunction): which activation function we will adjust our data by
            seed (int, optional): consistency is key! Try to use a seed to get repeatable data. Defaults to 0.
        """

        self.input_size = input_size
        self.activation_function = activation_function
        self.seed = seed

        self.recursion_predictions = np.array([])
        self.input_data = np.array([])

        # Setting a seed, so we can always reproduce results
        if self.seed:
            np.random.seed(self.seed)

        # We only want one output at a time, and we use that to recursively feed foward
        self.weights = np.random.rand(1, input_size)
        # Since we will always have an output size of 1, we want to have a bias of 1
        self.biases = np.random.rand(1, 1)

    def _forward_propagation(
        self, inputs: np.array, step_size: int = 0, is_training: bool = False
    ) -> np.array:
        """A function to recurently predict data

        Args:
            inputs (np.array): the data to start our model with
            step_size (int, optional): how far into the future to predict. Defaults to 0.
            is_training (bool, optional): an indicator letting us know if we need to store any data. Defaults to False.

        Returns:
            np.array: The predictions that the AI made
        """

        # if we are trainging, we want to store all of our predictions in a list, so we can adjust the model during back propigation
        if is_training:
            self.recursion_predictions = np.array([])
            self.input_data = inputs

        # Itterating over the stepsize to make a prediction, and then a followup prediction off of that prediction
        for _ in range(step_size):
            # forward prop
            prediction = self.activation_function.activation_function(
                np.dot(self.weights, inputs) + self.biases
            )

            # rolling our data and adding the prediction
            # ex.
            # [ 1, 2, 3 ] -> [ 2, 3, 1 ]
            #  pred 4 -> [2, 3, 4 ]
            inputs = np.roll(inputs, -1)
            inputs[-1] = prediction

            # if training we want to store our predictions
            if is_training:
                self.recursion_predictions = np.append(
                    self.recursion_predictions, prediction
                )

        return inputs

    def _backwards_propagation_through_time(
        self, error_derivatives: np.array, learning_rate: float = 0.1
    ):
        """A function to adjust the weights and biases of our RNN

        Args:
            error_derivatives (np.array): 2 * (prediction - target output) * actionvation_derivatives( prediction )
            learning_rate (float, optional): How fast to grow the model by. Defaults to .1.
        """
        # setting the weights and bias adjustment to 0
        weight_delta = 0
        bias_delta = 0

        # the error derivate should be a shape ( input_size, 1 )
        # we only want the want the final error derivate, because that is the predicted value
        # ex
        # with a step of 1, we get...
        # Input         : [ A, B, C ]
        #
        # Prediction    : [ B, C, P ]
        # Expected      ; [ B, C, D ]
        #
        # Notice how the error derivative for index, 0 and 1 are not needed, because we are not predicting with them
        # we are looking for the error of the last element that we should have gotten ( P & D )
        error_derivatives = error_derivatives[-1]

        # Itterating over the predictions and grabbing the updated error_derivatives until we reach the first prediction
        for index, prediction in enumerate(self.recursion_predictions[:-1]):
            '''
            When viewing back propigation through time, imagine that you are itterating over a model of that size. For instance...
            If I have a layer of 3 nodes, and I stepped forward 4 times in my prediction, my model can be represented as :

            W1
            W2
            W3

            in1 - h11 - h21 - h31 - out1
            in2 - h12 - h22 - h32 - out2
            in3 - h13 - h23 - h33 - out3

            each - represents a fully connected layer. This means that while we only have 1 set of weights and biases, we really
            made our model into a deep neural network by propigating the data forward 4 amount of times. 
            This also means, that in adjusting the weights and biases, 
            we too need to adjust them for the new 4 deep neural network that we created recurently
            '''
            # getting the input for the given state.
            # logic explained
            # predictions = [ 4, 5, 6 ]
            # input = [ 1, 2, 3 ]
            #
            # recursive predictions data = [ 4, 5 ]
            # since smaller than 3
            # recusive data inputs = [ 5, 4 ] join [ 3, 2, 1 ]
            # recusive data inputs = [ 5, 4, 3, 2, 1 ]
            # recusive data inputs = [ 5, 4, 3 ]
            #
            # if it was >= the size, we then just make sure that the predictions is the size
            recursive_input_data = self.recursion_predictions[ index + 1 : len(self.recursion_predictions) - 1 ]
            if len(recursive_input_data) < self.input_size:
                recursive_input_data = np.append(recursive_input_data[::-1], self.input_data[::-1])
                recursive_input_data = recursive_input_data[0 : self.input_size]
                recursive_input_data = recursive_input_data[::-1]
            else:
                recursive_input_data = recursive_input_data[0 : self.input_size]

            # Updating the weight and bias delta, before finding the new error derivative
            # We want to update a delta, because we still need the weights and biases that we used to predict our data in finding the new error derivative
            weight_delta += ( np.dot(np.array(recursive_input_data), error_derivatives) * learning_rate / len(self.recursion_predictions) )
            bias_delta += ( np.sum(error_derivatives, axis=0) * learning_rate / len(self.recursion_predictions) )

            # Calculating the new error derivative and grabbing its last elm (see comments above on why we want only the last elm)
            error_derivatives = np.dot( self.weights, error_derivatives ) * self.activation_function.activation_derivative(recursive_input_data)
            error_derivatives = [0][-1]

        # Updating the weight and bias delta
        weight_delta += (
            np.dot(np.array(self.input_data).T, error_derivatives)
            * learning_rate
            / len(self.recursion_predictions)
        )
        bias_delta += (
            np.sum(error_derivatives, axis=0)
            * learning_rate
            / len(self.recursion_predictions)
        )

        # updating the weights and biases by their delta
        self.weights -= np.array([weight_delta])
        self.biases -= bias_delta

    def predict_full(self, inputs: np.array, step_size: int = 0) -> np.array:
        """An abstracted function for forward propagation

        Args:
            inputs (np.array): The data that we are to predict off of
            step_size (int, optional): how far into the future to predict. Defaults to 0.

        Returns:
            np.array: an array that is the same size as the inputs. Containing the snippet of the final prediction(s)
        """
        _ = self._forward_propagation(
            inputs=np.array(inputs), step_size=step_size, is_training=True
        )
        return self.recursion_predictions

    def predict(self, inputs: np.array, step_size: int = 0) -> List[float]:
        """An abstracted function for forward propagation

        Args:
            inputs (np.array): The data that we are to predict off of
            step_size (int, optional): how far into the future to predict. Defaults to 0.

        Returns:
            List[float]: All of the predicted values from the start to the end of the step_size
        """
        return self._forward_propagation(inputs=inputs, step_size=step_size)

    def train(
        self,
        training_inputs: List[float],
        training_outputs: List[float],
        step_size: int = 0,
        learning_rate: float = 0.01,
    ):
        """An abstracted function of back propagation through time.

        Args:
            training_inputs (List[float]): The data that we are to predict off of
            training_outputs (List[float]): The data that we are to match
            step_size (int, optional): how far into the future to predict. Defaults to 0.
            learning_rate (float, optional): How fast to grow the model by. Defaults to .01.
        """
        # itterating  over a list of all of the training inputs and outputs
        for training_input, training_output in zip(training_inputs, training_outputs):
            # making a prediction
            prediction = self._forward_propagation(
                inputs=np.array(training_input), step_size=step_size, is_training=True
            )
            # calculating the error derivative
            error_derivatives = (
                2
                * (prediction - np.array(training_output))
                * self.activation_function.activation_derivative(prediction)
            )
            # adjusting the model
            self._backwards_propagation_through_time(
                error_derivatives=error_derivatives, learning_rate=learning_rate
            )

    def reset(self):
        """A function to rest the neural network"""
        self.recursion_predictions = np.array([])
        self.input_data = np.array([])

        if self.seed:
            np.random.seed(self.seed)
        # We only want one output at a time, and we use that to recursively feed foward
        self.weights = np.random.rand(1, self.input_size)
        # Since we will always have an output size of 1, we want to have a bias of 1
        self.biases = np.random.rand(1, 1)


"""
ACTIVATION FUNCTIONS
--------------------
"""


# Leaky Relu (BEST!!!)
def _leaky_relu(x, alpha=0.01):
    return np.maximum(x, alpha * x)


def _leaky_relu_derivative(x, alpha=0.01):
    dx = np.ones_like(x)
    dx[x < 0] = alpha
    return dx


LEAKY_RELU = ActivationFunction(
    activation_function=_leaky_relu, activation_derivative=_leaky_relu_derivative
)


# Relu
def _relu(x):
    return np.maximum(x, 0)


def _relu_derivative(x):
    return np.ones_like(x)


RELU = ActivationFunction(
    activation_function=_relu, activation_derivative=_relu_derivative
)


# Sigmoid
def _sigmoid(x):
    return 1 / (1 + np.exp(-x))


def _sigmoid_derivative(x):
    sigmoid_x = _sigmoid(x)
    return sigmoid_x * (1 - sigmoid_x)


SIGMOID = ActivationFunction(
    activation_function=_sigmoid, activation_derivative=_sigmoid_derivative
)

"""
GRAPHS
------
"""


def get_sin(size: int):
    return [(math.sin(x) + 1) / 2 for x in range(size)]


def get_y_x(size: int):
    return [float(x) / size for x in range(size)]


def get_sigmoid(size: int):
    return [_sigmoid(x / (size // 8)) for x in range(-(size // 2), (size // 2))]


def get_uber_2019_2022():
    # Open the CSV file
    # https://www.kaggle.com/datasets/varpit94/uber-stock-data
    # *NOTE* WARNING, this is not stock advice, this is to illistrate a use case for RNNs

    data = []

    REDUCE_RATIO = 10
    with open("UBER.csv", "r") as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)

        # Read the CSV file row by row
        for index, row in enumerate(csv_reader):
            if index % REDUCE_RATIO:
                continue
            # Concatenate all values in the row into a single string
            try:
                data.append((float(row[1]) - 25) / 40)
            except:
                continue

    return data


def get_training_in_out(
    data: List[float], input_size: int, step_size: int
) -> Tuple[List[float], List[float]]:
    """A function to turn 1 list into the input outputs needed for training

    Args:
        data (List[float]): the list that we have of Y points over X time
        input_size (int): how large the rnn input is
        step_size (int): how far into the future to make the prediction per model

    Returns:
        Tuple[List[float], List[float]]: training inputs and outputs
    """
    inputs = []
    outputs = []
    for index in range(len(data[: -(input_size + step_size - 1)])):
        inputs.append(list(data[index : index + input_size]))
        outputs.append(list(data[index + step_size : index + step_size + input_size]))

    return inputs, outputs

def main():
    INPUT_SIZE = 16
    STEP_SIZE = 1
    LEARNING_RATE = 0.01
    EPOCHES = 100
    PREDICT_LENGTH = 30

    rnn = RecursiveNeuralNetwork(
        input_size=INPUT_SIZE, 
        activation_function=LEAKY_RELU, 
        seed=1
    )

    data = get_uber_2019_2022()  # get_sin(INPUT_SIZE*2)

    training_inputs, training_outputs = get_training_in_out(data, INPUT_SIZE, STEP_SIZE)

    for _ in range(EPOCHES):
        rnn.train(
            training_inputs=training_inputs,
            training_outputs=training_outputs,
            step_size=STEP_SIZE,
            learning_rate=LEARNING_RATE,
        )
        time.sleep(0.01)

    # Creating the plot
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    # Full Data Graph
    axes[0, 0].plot([i for i in range(len(data))], data, label="Full Data")
    axes[0, 1].set_title("True Data")
    axes[0, 0].legend() 
    # AI vs Expected Start
    guess = rnn.predict_full( inputs=np.array(training_inputs[0]), step_size=PREDICT_LENGTH )
    axes[0, 1].plot( [i for i in range(PREDICT_LENGTH + len(training_inputs[0]))], np.append(training_inputs[0], guess), label="AI", )
    axes[0, 1].plot( [i for i in range(len(training_inputs[0]))], training_inputs[0], label="Given" )
    axes[0, 1].set_title("Plot of AI and Expected Start")
    axes[0, 1].legend()
    # AI vs Expected MidPoint
    guess2 = rnn.predict_full(inputs=np.array( training_inputs[len(training_inputs) // 2]), step_size=PREDICT_LENGTH, )
    axes[1, 0].plot( [i for i in range(PREDICT_LENGTH + len(data) // 2)], np.append(data[: len(data) // 2], guess2), label="AI", )
    axes[1, 0].plot( [i for i in range(len(data[: len(data) // 2]))], data[: len(data) // 2], label="Given", )
    axes[1, 0].set_title("Plot of AI and Expected MidPoint")
    axes[1, 0].legend()  # Display legend
    # AI vs Expected End
    guess3 = rnn.predict_full( inputs=np.array(training_outputs[-1]), step_size=PREDICT_LENGTH )
    axes[1, 1].plot( [i for i in range(PREDICT_LENGTH + len(data))], np.append(data, guess3), label="AI", )
    axes[1, 1].plot([i for i in range(len(data))], data, label="Given")
    axes[1, 1].set_title("Plot of AI and Expected End")
    axes[1, 1].legend()  # Display legend

    plt.show()


if __name__ == "__main__":
    main()