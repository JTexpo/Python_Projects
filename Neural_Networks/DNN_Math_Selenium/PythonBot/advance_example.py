from deep_neural_network import DeepNeuralNetwork, LEAKY_RELU
import numpy as np
import random


def free_fall(initial_position, velocity, time):
    return initial_position + (velocity * time) - (0.5 * 9.81 * (time**2))


if __name__ == "__main__":
    """
    Do Not Be Fooled By The Simplicity Of This Project!

    While this is a simple example to show a 2 In 1 Out solution, we can take more advance formulas too and train the AI.
    In Physics the free fall equation is...

    final_position = initial_position + initial_velocity * time + .5 * acceleration (gravity = -9.81) * time ^ 2
    """

    # Creating a DNN
    my_dnn = DeepNeuralNetwork(
        input_size=3,
        output_size=1,
        hidden_layers=[12, 6],
        activation_function=LEAKY_RELU,
        random_seed=1,
    )

    # Setting everything to be the same each itteration, so you can see what I see
    random.seed(1)

    # 10 sets of 100 new data to train on, this should make the AI very smart. That is in total 1_000 items to be trained on
    for _ in range(10):
        data_inputs = []
        data_outputs = []

        for _ in range(100):
            initial_position, velocity, time = (
                random.randint(30, 40),
                random.randint(0, 3),
                random.randint(1, 2),
            )
            data_inputs.append(
                [[(initial_position - 29) / 10.0, (velocity) / 3.0, (time) / 2.0]]
            )
            data_outputs.append([[free_fall(
                            initial_position=initial_position,
                            velocity=velocity,
                            time=time,
                        ) / 40]])

        # Training for only 50, because there is a lot to train, and I dont want to be here for forever
        my_dnn.train(
            training_inputs=np.array(data_inputs),
            training_outputs=np.array(data_outputs),
            epochs=50,
            learning_rate=0.01,
        )

    # And now...
    random.seed(1)
    initial_position, velocity, time = (
        random.randint(30, 40),
        random.randint(0, 3),
        random.randint(1, 2),
    )
    dnn_answer = (
        my_dnn.forward_propagation(
            np.array([(initial_position - 29) / 10.0, (velocity) / 3.0, (time) / 2.0]))[0][0]* 40
    )
    true_answer = free_fall(
        initial_position=initial_position, velocity=velocity, time=time
    )
    print(
        f"""VALUES
------
initial_position    = {initial_position} 
velocity            = {velocity}
time                = {time}

ANSWERS
-------
DNN     : {dnn_answer}
TRUE    : {true_answer}

ERROR
-----
Delta   (dnn - true)  = {dnn_answer - true_answer}
Loss    (Delta)^2     = {(dnn_answer - true_answer)**2}"""
    )

# Incase you dont have a computer to run this or are too lazy
#
#
# VALUES
# ------
# initial_position    = 32
# velocity            = 0
# time                = 2
#
# ANSWERS
# -------
# DNN     : 12.524778967004393
# TRUE    : 12.379999999999999
#
# ERROR
# -----
# Delta   (dnn - true)  = 0.14477896700439352
# Loss    (Delta)^2     = 0.02096094928685927
