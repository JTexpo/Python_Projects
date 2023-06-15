from deep_neural_network import DeepNeuralNetwork, LEAKY_RELU

from webscrapper import WebScrapper

import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By

QUESTIONS_PULLED = 20
QUESTIONS_ANSWERED = 10


def get_user_math_selection() -> str:
    while True:
        user_input = input(
            "Please select which math questions you would like to solve.\n1. Addition\n2. Subtraction\n3. Multiplication\n4. Division\n:"
        )
        if "quit" in user_input.lower():
            quit()
        elif ("1" in user_input) or ("add" in user_input.lower()):
            return "addition"
        elif ("2" in user_input) or ("sub" in user_input.lower()):
            return "subtraction"
        elif ("3" in user_input) or ("mul" in user_input.lower()):
            return "multiplication"
        elif ("4" in user_input) or ("div" in user_input.lower()):
            return "division"
        print("Sorry, please enter either the number or the word of one of the topics.")


def addition_dnn_solve(
    web_bot: WebScrapper, questions_pulled: int = 100, questions_answer: int = 100
):
    dnn = DeepNeuralNetwork(
        input_size=2,
        output_size=1,
        hidden_layers=[],
        activation_function=LEAKY_RELU,
        random_seed=1,
    )

    data_inputs, data_outputs = web_bot.get_addition_data(
        size=questions_pulled,
        data_inputs_grooming=lambda x : float(x)/10.0,
        data_outputs_grooming=lambda x : float(x)/20.0,
    )

    dnn.train(
        training_inputs=np.array(data_inputs),
        training_outputs=np.array(data_outputs),
        epochs=50,
        learning_rate=0.1,
    )

    answers = web_bot.answer_addition_questions(
        dnn=dnn,
        data_inputs_grooming=lambda x : float(x)/10.0,
        data_outputs_grooming=lambda x : float(x)*20.0,
        amount=questions_answer,
    )

    print(f"{answers}/{questions_answer} = {round((answers/questions_answer)*100)}%")


def subtraction_dnn_solve(
    web_bot: WebScrapper, questions_pulled: int = 100, questions_answer: int = 100
):
    dnn = DeepNeuralNetwork(
        input_size=2,
        output_size=1,
        hidden_layers=[],
        activation_function=LEAKY_RELU,
        random_seed=1,
    )

    data_inputs, data_outputs = web_bot.get_subtraction_data(
        size=questions_pulled,
        data_inputs_grooming=lambda x : float(x)/10.0,
        data_outputs_grooming=lambda x : (float(x)+10)/20.0,
    )

    dnn.train(
        training_inputs=np.array(data_inputs),
        training_outputs=np.array(data_outputs),
        epochs=50,
        learning_rate=0.1,
    )

    answers = web_bot.answer_subtraction_questions(
        dnn=dnn,
        data_inputs_grooming=lambda x : float(x)/10.0,
        data_outputs_grooming=lambda x : float(x)*20.0-10,
        amount=questions_answer,
    )

    print(f"{answers}/{questions_answer} = {round((answers/questions_answer)*100)}%")

def multiplication_dnn_solve(
    web_bot: WebScrapper, questions_pulled: int = 100, questions_answer: int = 100
):
    dnn = DeepNeuralNetwork(
        input_size=2,
        output_size=1,
        hidden_layers=[],
        activation_function=LEAKY_RELU,
        random_seed=1,
    )

    data_inputs, data_outputs = web_bot.get_multiplication_data(
        size=questions_pulled,
        data_inputs_grooming=lambda x : np.log(float(x))/3.0,
        data_outputs_grooming=lambda x : np.log(float(x))/5.0,
    )

    dnn.train(
        training_inputs=np.array(data_inputs),
        training_outputs=np.array(data_outputs),
        epochs=100,
        learning_rate=0.1,
    )

    answers = web_bot.answer_multiplication_questions(
        dnn=dnn,
        data_inputs_grooming=lambda x : np.log(float(x))/3.0,
        data_outputs_grooming=lambda x : np.e ** (float(x)*5.0),
        amount=questions_answer,
    )

    print(f"{answers}/{questions_answer} = {round((answers/questions_answer)*100)}%")

def division_dnn_solve(
    web_bot: WebScrapper, questions_pulled: int = 100, questions_answer: int = 100
):
    dnn = DeepNeuralNetwork(
        input_size=2,
        output_size=1,
        hidden_layers=[],
        activation_function=LEAKY_RELU,
        random_seed=1,
    )

    data_inputs, data_outputs = web_bot.get_division_data(
        size=questions_pulled,
        data_inputs_grooming=lambda x : np.log(float(x))/3.0,
        data_outputs_grooming=lambda x : (np.log(float(x))+3.0)/6.0,
    )

    dnn.train(
        training_inputs=np.array(data_inputs),
        training_outputs=np.array(data_outputs),
        epochs=300,
        learning_rate=0.1,
    )

    answers = web_bot.answer_division_questions(
        dnn=dnn,
        data_inputs_grooming=lambda x : np.log(float(x))/3.0,
        data_outputs_grooming=lambda x : np.e ** ((float(x)*6.0)-3),
        amount=questions_answer,
    )

    print(f"{answers}/{questions_answer} = {round((answers/questions_answer)*100)}%")


if __name__ == "__main__":
    web_bot = WebScrapper(
        # On VScode there is a beautiful extension called :
        # Live Server by Ritwick Dey
        # For me, Live Server deploys to localhost http://127.0.0.1:5500, this may be different for you
        url="http://127.0.0.1:5500/Webpage/index.html",
        # The reason why I use Safari is because it comes with Selenium by default. You can always dowload other drivers, but I tried to use as little dependencies as possible
        driver=webdriver.Safari(),
        by_xpath=By.XPATH,
    )

    while True:
        user_input = get_user_math_selection()
        if user_input == "addition":
            addition_dnn_solve(
                web_bot=web_bot,
                questions_pulled=QUESTIONS_PULLED,
                questions_answer=QUESTIONS_ANSWERED,
            )
        elif user_input == "subtraction":
            subtraction_dnn_solve(
                web_bot=web_bot,
                questions_pulled=QUESTIONS_PULLED,
                questions_answer=QUESTIONS_ANSWERED,
            )
        elif user_input == "multiplication":
            multiplication_dnn_solve(
                web_bot=web_bot,
                questions_pulled=QUESTIONS_PULLED,
                questions_answer=QUESTIONS_ANSWERED,
            )
        elif user_input == "division":
            division_dnn_solve(
                web_bot=web_bot,
                questions_pulled=QUESTIONS_PULLED,
                questions_answer=QUESTIONS_ANSWERED,
            )