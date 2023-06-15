import numpy as np
import time

class ActivationFunction:
    def __init__(self, activation_function: callable, activation_derivative: callable):
        self.activation_function = activation_function
        self.activation_derivative = activation_derivative


class DeepNeuralNetwork:
    def __init__(
        self,
        input_size: int,
        output_size: int,
        hidden_layers: list,
        activation_function: ActivationFunction,
        random_seed: int = 0,
    ):
        """A class for our Deep Neural Network

        Args:
            input_size (int): How many input nodes there are
            output_size (int): How many outputs we expect
            hidden_layers (list): A list that contains the hidden layers and their nodes
                [
                    4, # would indicate a hidden layer of 1 with 4 nodes
                    2, # would indicate a second hidden layer of 2 with 2 nodes
                ]
            activation_function (ActivationFunction): A function which will be used as well as its derivative
            random_seed (int, optional): Consistency is key, and this helps control that. Defaults to 0.
        """
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_layers = hidden_layers
        self.activation_function = activation_function
        self.random_seed = random_seed
        # if a random seed is provided, we set the seed before generating all of the weights and biases
        if random_seed:
            np.random.seed(self.random_seed)

        self.weights = []
        self.biases = []

        current_layer = input_size
        for layer in hidden_layers:
            '''
            We want to create a 2d array of the dimensions ( current layer, layer )
            this is because when we connect everything together it will look like...
            ex.

            Given that we have the following params 
            self.input_size = 2
            self.output_size = 1
            self.hidden_layers = 3

            the weight size should be..
            (2,3)(3,1)

            This will allow the weights to interact with the inputs and outputs so that
            Input 2 (2,3)(3,1) 1 Output
            '''
            self.weights.append(np.random.rand(current_layer, layer))
            '''
            Unlike the weights, the biases do not expect an input. 
            These will always be of the dimensions ( 1, layer ).
            This is because the biases exist on the same layer as the weights and will only be used a layer amount of times
            ex.

            Dot Product(Node * Weight) + Bias = Next Node

            The Biases will be added to the dot product so that...

                ([ 1, 2, 3] [[4],)
            DOT(             [5], ) = [32] 
                (            [6]])

            then... [32] + Bias

            This is using a 1x3 and 3x1 ; however, the idea scales for any size
            '''
            self.biases.append(np.random.rand(1, layer))
            # updating the current layer to be the layer of the hidden layer. This is to help with that pattern of
            # (old layer, layer) (layer , new layer)
            current_layer = int(layer)
        # Doing everything above, but now not for the hidden layer, but for the output
        self.weights.append(np.random.rand(current_layer, output_size))
        self.biases.append(np.random.rand(1, output_size))

    def forward_propagation(
        self, input_data: np.array, is_training: bool = False
    ) -> np.array or list:
        """Computing the prediction

        Args:
            input_data (np.array): the input data, must be the same size as self.input_size
            is_training (bool): indicates if we need to return back the np.array or the list (which holds all of the np.array predictions)

        Returns:
            np.array: the out_put predictions
            or
            list: this is a list of the np.array, for training purposes
        """
        list_of_input_data = []
        for bias, weight in zip(self.biases, self.weights):
            '''
            forward propagation means to send forward. We are sending forward the data that we hold until we reach the end of our DNN.
            Each itteration that the data moves forwards it is impacted by the weights and biases of that layer.
            '''
            input_data = self.activation_function.activation_function(np.dot(input_data, weight) + bias)
            # If we are looking to train we need to retain the input data for training purposes, else we can move forward and not worry (saving some memory space)
            if is_training:
                list_of_input_data.append(input_data.copy())
        # For training we need to return all of the input_data history so we can annalyze where we were wrong with the chain rule
        if is_training:
            return list_of_input_data
        # Retruns an array containing the data
        return input_data

    def backwards_propagation(
        self,
        input_data: np.array,
        predictions: list,
        target_output: np.array,
        learning_rate: float,
    ):
        """Adjusting the weights and biases based on the correct output.

        ... lets put on our calc boots

        Args:
            input_data (np.array): The data that we were given
            predictions (list): This is a list of np.array, the data that we produced
            target_output (np.array): The expected data that we were to generate
            learning_rate (float): How quickly we want to adjust our model
        """
        # A loss function is = (target_output - prediction)^2 , the error is the derivative of the loss function
        output_error = 2 * (target_output - predictions[-1])
        # We are now taking the derivative of our output and multiplying it by our output error. 
        # This is because it will give us a delta to preform a dot product against our predictions with, letting us know how far off our weights (and biases) are
        error_derivatives = (output_error * self.activation_function.activation_derivative(target_output))

        '''
        Lots of tutorials online stores each values of their DNNs as a value and then manually preform this step per-layer;
        however, similar to our forward propagation, after we preform the logic, we do not need to allocate memory for this step.
        This code allows for our memory to be better managed and in turn run faster!

        We want to itterate throughout our predictions inversed, without the last element. 
        This is because the last element is the output, and is not checked against our weights. The common pattern for back propagation is...

        error = 2*(target_output - our_output)
        delta = error * activation_derivative(target_output)

        delta_weight3 = np.dot(layer2.T, delta)

        new_error = dot(delta, weight3)
        new_delta = new_error * activation_derivative(layer2)

        delta_weight2 = np.dot(layer1.T, new_delta)

        new_error2 = dot(new_delta, .weight2)
        new_delta2 = new_error2 * activation_derivative(layer1)
        
        delta_weight1 = np.dot(input.T, new_delta2)

        weight3 += delta_weight3
        weight2 += delta_weight2
        weight1 += delta_weight1

        As we can see, the logic for the delta of weight 3 and 2 are similar, relying on the layer above to preform the dot product with the previous error.
        You may also notice that the new_error{n+1} is dependent on the new_error{n}, this is because of a math concept known as the chain rule. 
        '''
        for reverse_index, prediction in enumerate(predictions[::-1][1:]):
            # Calculating the 'new_error{n+1}' as referenced in the comments above
            temp_error_derivatives = np.dot(error_derivatives, self.weights[-(reverse_index + 1)].T) * self.activation_function.activation_derivative(prediction)
            # Reverse_index + 1 because, reverse starts at index 0 and to itterate through weights & biases backwards we need to start at index -1
            self.weights[-(reverse_index + 1)] += (np.dot(np.array(prediction).T, error_derivatives) * learning_rate)
            self.biases[-(reverse_index + 1)] += (np.sum(error_derivatives, axis=0) * learning_rate)
            # Moving the temp value into the new_error.
            # The reson why we cant make this in one line, is because the temp_error relies on the weights, and we update the weights on the line after
            error_derivatives = temp_error_derivatives.copy()
        # Preforming the same logic above, but now with the input and not the weights
        self.weights[0] += np.array(np.dot(input_data.T, error_derivatives) * learning_rate)
        self.biases[0] += np.sum(error_derivatives, axis=0) * learning_rate

        return
    
    def train(
        self,
        training_inputs: np.array,
        training_outputs: np.array,
        epochs: int,
        learning_rate: float = 0.1,
    ):
        """A function to train the DNN. This is an abstraction of the two function above, the :
                forward_propagation
                &
                backwards_propagation
            This is because to train, just like in real-life, we need to attempt and reflect.

        Args:
            training_inputs (np.array): A list of inputs 
            training_outputs (np.array): A list of output matched 1:1 to their inputs
            epochs (int): How many itterations to train for
            learning_rate (float, optional): How quick we want the model to learn. Defaults to 0.1.
        """
        for _ in range(epochs):
            for input_data, target_output in zip(training_inputs, training_outputs):
                predictions = self.forward_propagation(input_data, True)
                self.backwards_propagation(input_data, predictions, target_output, learning_rate)
            time.sleep(0.02)
        return

'''
ACTIVATION FUNCTIONS
--------------------
'''

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
    return np.maximum(x,0)

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


if __name__ == "__main__":
    '''
    ADDITION
    --------
    DATA :

    data_inputs = []
    data_outputs = []
    for x in range(9):
        for y in range(9):
            data_inputs.append([[(x + 1) / 10.0, (y + 1) / 10.0]])
            data_outputs.append([[((x + 1) + (y + 1)) / 20.0]])

    # Train AI Here

    for data_input in data_inputs:
        print(f"{data_input[0][0]*10} * {data_input[0][1]*10} = {my_dnn.forward_propagation(np.array(data_input))[0][0] * 20}")

    DNN :
    input_size=2,
    output_size=1,
    hidden_layers=[],
    activation_function=LEAKY_RELU,
    random_seed=1,
    
    TRAIN :
    training_inputs=np.array(data_inputs),
    training_outputs=np.array(data_outputs),
    epochs=10,
    learning_rate=.1
    NOTE : This will result where there will need to be a rounding aid of the 1ths place to be 100% accurate

    EXPECTED WEIGHTS & BIASES :
    Weights - [ array([[0.49999828],[0.50000003]]) ]
    Biases - [ array([[1.52102046e-06]]) ]
    NOTE : 
    This makes sense because the divisor for the output is double the size then the divisors for the inputs.
    This means that if we change our data_inputs to be : 

    data_inputs.append([[(x + 1) / 20.0, (y + 1) / 20.0]])

    Then we would expect for our weights to be close to [ array([[1],[1]]) ] , due to the inputs sharing a 1 to 1 divisor with the outputs.
    This may raise the question of "why do we divide our input by 20.0 and not just divide them by 1?"
    This is a great question, and is answered by : we want to normalize our data as best as we can. Weights and Biases can exceed 1; however,
    it is common practice for them to start within the range of 0 -> 1 and grow at a rate relative to the learning_rate (.1 in our example). 
    Dividing everything by 10 & 20 allows for the data to be within that 0 -> 1 range, and thus allows for the learning to be optimized for the best model.
    
    In addition, training is not product. So long as we normalize all of our inputs by dividng by 10, our model can be for an infinite range.
    ex :

    print(my_dnn.forward_propagation(np.array([2,2]))[0] * 20) 
    >>> 40

    Finally if we were to change the formula to be :

    data_outputs.append([[((x + 1) + (y + 1) + 5 ) / 20.0]])
    
    we could expect something along the lines of Weights = [ array([[0.5],[0.5]]) ] & Biases = [ array([[5]]) ]



    SUBTRACTION
    -----------
    DATA :

    data_inputs = []
    data_outputs = []
    for x in range(9):
        for y in range(9):
            data_inputs.append([[(x + 1) / 10.0, (y + 1) / 10.0]])
            data_outputs.append([[((x + 1) - (y + 1) + 10) / 20.0]])
    
    # Train AI Here
    
    for data_input in data_inputs:
        print(f"{data_input[0][0]*10} - {data_input[0][1]*10} = {my_dnn.forward_propagation(np.array(data_input))[0][0] * 20 - 10}")

    DNN :
    input_size=2,
    output_size=1,
    hidden_layers=[],
    activation_function=LEAKY_RELU,
    random_seed=1,

    TRAIN :
    training_inputs=np.array(data_inputs),
    training_outputs=np.array(data_outputs),
    epochs=50,
    learning_rate=.1
    NOTE : This will result where there will need to be a rounding aid of the 1ths place to be 100% accurate

    EXPECTED WEIGHTS & BIASES :
    Weights - [ array([[ 0.50000939],[-0.50000017]]) ]
    Biases - [ array([[0.49999169]]) ]
    NOTE : 
    This makes sense for similar reasons as the ADDITION category. The .5 is due to the divisor being 10, and not 20, and the negative is due to testing subtraction
    We can expect that if we were to flip from x - y to y - x, then we would have a negative weight in the x index (0)


    MULTIPLICATION & DIVISION
    -------------------------
    Uh-oh, theres nothing here... well that's because I'm not the smartest person in the world. 
    There exists a Universal Approximation Theorem, which states that Multiplication is possible with an infinite amount of nodes in a single hidden layer.

    To point you into the right direction, with a hidden layer of [16], you can have very exeptional results!
    Best of luck finding the number between one and infinity which best fits for multiplication & division

    Link to learn more : https://en.wikipedia.org/wiki/Universal_approximation_theorem

    AMAZING LINK FOR DNNs WITH PYTHON : https://towardsdatascience.com/how-to-build-your-own-neural-network-from-scratch-in-python-68998a08e4f6


    ... However~
    m = x*y => ln(m) = ln(x) + ln(y) ; for x & y > 0
    NOTE : Mathematicians are awesome, and this means that we 'can' do multiplication, our grooming of the data looks slightly interesting

    '''
    data_inputs = []
    data_outputs = []
    for x in range(9):
        for y in range(9):
            data_inputs.append([[np.log(x + 1), np.log(y + 1)]])
            data_outputs.append([[(np.log(x + 1) + np.log(y + 1)) / 5.0]])
    
    my_dnn = DeepNeuralNetwork(
        input_size=2,
        output_size=1,
        hidden_layers=[],
        activation_function=LEAKY_RELU,
        random_seed=1,
    )
    my_dnn.train(
        training_inputs=np.array(data_inputs),
        training_outputs=np.array(data_outputs),
        epochs=10,
        learning_rate=.1
    )
    for data_input in data_inputs:
        print(f"{np.e**data_input[0][0]} * {np.e**data_input[0][1]} = {np.e**(my_dnn.forward_propagation(np.array(data_input))[0][0] * 5)}")