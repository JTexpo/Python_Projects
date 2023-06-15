import numpy as np

import random
from typing import Optional


def piecewise_linear(x: float)->float:
    """An activation functiont that has the bounds of -1 and 1

    Args:
        x (float): the x value

    Returns:
        float: -1 -> 1, all inclusive
    """
    if x < -1:
        return -1
    if x > 1:
        return 1
    return x

# a numpy qol that alows for a function to be applied across an array
VECTORIZED_PIECEWISE_LINEAR = np.vectorize(piecewise_linear)


class NeuralNetwork:
    def __init__(
        self,
        seed: Optional[int] = None,
        input_layer_weights: Optional[np.array] = None,
        input_layer_biases: Optional[np.array] = None,
        output_layer_weights: Optional[np.array] = None,
        output_layer_biases: Optional[np.array] = None,
        noise: Optional[float] = None,
    ):
        """A class for our neural netowkr since there will be a lot!
        
        I will fully connect this; however, I theorize that if the model achieves optimal preformance
        if it ends up evolving into something like: 

        nearest_coin_y_center   \
                                  best_coin_move ( 0 < fall ; 0 > fly )  \
                                /                                         \
        player_y                                                            action ( 0 < fall ; 0 > fly )
                                \                                         /
        zapper_y_top            - best_safety_move ( 0 < fall ; 0 > fly )/
        zapper_y_bottom         /

        Args:
            seed (Optional[int], optional): consistency is key. Defaults to None.
            input_layer_weights (Optional[np.array], optional): if a weight is provided then it the neural network will adopt it; however, if not it will create its own. Defaults to None.
            input_layer_biases (Optional[np.array], optional): if a bias is provided then it the neural network will adopt it; however, if not it will create its own. Defaults to None.
            output_layer_weights (Optional[np.array], optional): if a weight is provided then it the neural network will adopt it; however, if not it will create its own. Defaults to None.
            output_layer_biases (Optional[np.array], optional): if a bias is provided then it the neural network will adopt it; however, if not it will create its own. Defaults to None.
            noise (Optional[float], optional): any amount of noise to modify the weight and bias by upon creation. Defaults to None.
        """

        # randomness is good, but most importantly we want controlled randomness
        self.seed = seed
        if seed:
            np.random.seed(seed)

        # Setting the weights and biases
        self.input_layer_weights = (
            input_layer_weights  if input_layer_weights is not None else np.random.rand(4, 2)-.5
        )
        self.input_layer_biases = (
            input_layer_biases  if input_layer_biases is not None else np.random.rand(1, 2)-.5
        )
        self.output_layer_weights = (
            output_layer_weights if output_layer_weights is not None else np.random.rand(2, 1)-.5 
        )
        self.output_layer_biases = (
            output_layer_biases if output_layer_biases is not None else np.random.rand(1, 1)-.5 
        )

        # Adding noise to the weights and biases
        if noise is not None:
            self.input_layer_weights += (np.random.rand(4, 2)-.5) * noise
            self.input_layer_biases += (np.random.rand(1, 2)-.5) * noise
            self.output_layer_weights += (np.random.rand(2, 1)-.5) * noise
            self.output_layer_biases += (np.random.rand(1, 1)-.5) * noise

    def forward_propagate(
        self,
        nearest_coin_y_center: float,
        player_y: float,
        zapper_y_top: float,
        zapper_y_bottom: float,
    ) -> float:
        """A function to allow for the neural network to predict its action given a gamestate

        Args:
            nearest_coin_y_center (float): y axis of coin within the bounds of 0->1
            player_y (float): y axis of player within the bounds of 0->1
            zapper_y_top (float): y axis of top zapper within the bounds of 0->1
            zapper_y_bottom (float): y axis of bottom zapper within the bounds of 0->1

        Returns:
            float: the prediction for the game state 
                RANGE: -1 -> 1
        """
        # this is may be very intimidating; however, since forward propagation is just a loop, I condenced the loop into
        # a single string to allow for no more memory to be alocated then needed
        return VECTORIZED_PIECEWISE_LINEAR(
            np.dot(
                VECTORIZED_PIECEWISE_LINEAR(
                    np.dot(
                        np.array(
                            [[
                                nearest_coin_y_center,
                                player_y,
                                zapper_y_top,
                                zapper_y_bottom,
                            ]]
                        ),
                        self.input_layer_weights,
                    )
                    + self.input_layer_biases
                ),
                self.output_layer_weights,
            )
            + self.output_layer_biases
        )[0][0]


def shuffle_2d(
    array1: np.array, array2: np.array, seed: Optional[int] = None
) -> np.array:
    """A function to mix 2 2D arrays together

    Args:
        array1 (np.array): ex. [ [ 1, 2 ], [ 3, 4 ] ]
        array2 (np.array): ex. [ [ 5, 6 ], [ 7, 8 ] ]
        seed (Optional[int], optional): randomness is important, but so is consistency. Defaults to None.

    Returns:
        np.array: a shuffled array
            ex. [ [ 1, 6 ], [ 7, 4 ] ]
    """
    # setting the seed
    if seed:
        random.seed(seed)

    # returning a random 2d array
    return np.array(
        [
            [random.choice([a, b]) for a, b in zip(row1, row2)]
            for row1, row2 in zip(array1, array2)
        ]
    )


def generate_offspring(
    neural_network1: NeuralNetwork,
    neural_network2: NeuralNetwork,
    seed: Optional[int] = None,
    noise: Optional[float] = None,
) -> NeuralNetwork:
    """A function to take 2 neural networks and create an offspring of similar weights and biases shuffled around.

    Args:
        neural_network1 (NeuralNetwork): the first Neural Network
        neural_network2 (NeuralNetwork): the second Neural Network
        seed (Optional[int], optional): randomness is important, but so is consistency. Defaults to None.
        noise (Optional[float], optional): any modification to be applied to the offsprince. Defaults to None.

    Returns:
        NeuralNetwork: A neural network similar to the two provided
    """
    return NeuralNetwork(
        seed=seed,
        input_layer_weights=shuffle_2d(
            neural_network1.input_layer_weights,
            neural_network2.input_layer_weights,
            seed=seed,
        ),
        input_layer_biases=shuffle_2d(
            neural_network1.input_layer_biases,
            neural_network2.input_layer_biases,
            seed=seed,
        ),
        output_layer_weights=shuffle_2d(
            neural_network1.output_layer_weights,
            neural_network2.output_layer_weights,
            seed=seed,
        ),
        output_layer_biases=shuffle_2d(
            neural_network1.output_layer_biases,
            neural_network2.output_layer_biases,
            seed=seed,
        ),
        noise=noise,
    )
