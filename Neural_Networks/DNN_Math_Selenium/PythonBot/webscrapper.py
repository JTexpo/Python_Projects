import time
import numpy as np
from typing import Tuple
from selenium import webdriver

from deep_neural_network import DeepNeuralNetwork


class WebScrapper:
    def __init__(self, url: str, driver: webdriver, by_xpath: str):
        self.url = url
        self.driver = driver
        self.by_xpath = by_xpath

        self.driver.get(self.url)

        self.addition_button_xpath = '//*[@id="operator-buttons"]/button[1]'
        self.answer_text_box_xpath = '//*[@id="answer"]'
        self.answer_response_xpath = '//*[@id="result"]'
        self.division_button_xpath = '//*[@id="operator-buttons"]/button[4]'
        self.math_question_xpath = '//*[@id="question"]'
        self.multiplication_button_xpath = '//*[@id="operator-buttons"]/button[3]'
        self.submit_button_xpath = '//*[@id="submit"]'
        self.subtraction_button_xpath = '//*[@id="operator-buttons"]/button[2]'

    def _collect_data(
        self,
        size: int,
        data_inputs_grooming: callable,
        data_outputs_grooming: callable,
        sleep: float = 0.1,
    ) -> Tuple[list, list]:
        """A function to grab the questions and their answers for a math question

        Args:
            size (int): How many questions and their answers you want to grab
            data_inputs_grooming (callable): A function to transform our data inputs
            data_outputs_grooming (callable): A function to transform our data outputs
            sleep (float, optional): _description_. Defaults to 0.1.

        Returns:
            Tuple[list,list]:
                data_inputs : a list of all of the inputs. Schema :
                    [
                        [
                            [ input_1, input_2 ]
                        ],
                        [
                            [ input_3, input_4 ]
                        ],
                        ...
                    ]
                data_outputs : a list of all of the outputs. Schema :
                    [
                        [
                            [ output_1 ]
                        ],
                        [
                            [ output_2 ]
                        ],
                        ...
                    ]
        """
        data_inputs = []
        data_outputs = []

        for _ in range(size):
            # Finding and tokenizing math question
            math_question = self.driver.find_element(
                self.by_xpath, self.math_question_xpath
            )
            tokenize_math_question = math_question.text.split(" ")

            # Sending knowingly wrong answer to speed up gathering results
            text_box = self.driver.find_element(
                self.by_xpath, self.answer_text_box_xpath
            )
            text_box.send_keys("-100")

            # Submitting answer
            submit_button = self.driver.find_element(
                self.by_xpath, self.submit_button_xpath
            )
            self.driver.execute_script("arguments[0].click();", submit_button)

            # Finding correct answer
            answer_response = self.driver.find_element(
                self.by_xpath, self.answer_response_xpath
            )

            # adding the fields to input
            data_inputs.append(
                [
                    [
                        data_inputs_grooming(tokenize_math_question[0]),
                        data_inputs_grooming(tokenize_math_question[-1]),
                    ]
                ]
            )
            data_outputs.append(
                [[data_outputs_grooming(answer_response.text.split(" ")[-1][:-1])]]
            )

            time.sleep(sleep)

        return data_inputs, data_outputs

    def _answer_questions(
        self,
        dnn: DeepNeuralNetwork,
        data_inputs_grooming: callable,
        data_outputs_grooming: callable,
        round_answer: int,
        amount: int,
        operation: str,
        sleep: float = 0.1,
    ) -> int:
        """A function to answer the math questions on the webpage

        Args:
            dnn (DeepNeuralNetwork): A deep neural network. More info in deep_neural_network.py
            data_inputs_grooming (callable): A function to transform our data inputs
            data_outputs_grooming (callable): A function to transform our data outputs
            round_answer (int): The A in AI stands for artificial, and sometimes there is some handicaps needed.
                This varible will help round to the Nth place
            amount (int): How many questions you want to answer
            operation (str): A visual display in the consol logs
            sleep (float, optional): How long the computer should rest before itterating another step.
                .1 is what most tools like pyautogui use, so I too believe it is a good amount
        Returns:
            int: the amount of successfully answered questions
        """

        success_count = 0

        for _ in range(amount):
            # Finding and tokenizing math question
            math_question = self.driver.find_element(
                self.by_xpath, self.math_question_xpath
            )
            tokenize_math_question = math_question.text.split(" ")

            # Collecting the answer from our DNN
            answer = data_outputs_grooming(
                dnn.forward_propagation(
                    input_data=np.array(
                        [
                            [
                                data_inputs_grooming(tokenize_math_question[0]),
                                data_inputs_grooming(tokenize_math_question[-1]),
                            ]
                        ]
                    )
                )[0][0]
            )
            answer = round(answer, ndigits=round_answer)

            # Sending the answer to the text box
            text_box = self.driver.find_element(
                self.by_xpath, self.answer_text_box_xpath
            )
            text_box.send_keys(answer)

            # Submitting the answer
            submit_button = self.driver.find_element(
                self.by_xpath, self.submit_button_xpath
            )
            self.driver.execute_script("arguments[0].click();", submit_button)

            # Checking the response to see if our DNNs prediction was correct
            answer_response = self.driver.find_element(
                self.by_xpath, self.answer_response_xpath
            )
            if "correct!" in answer_response.text.lower():
                success_count += 1
            print(
                f"{tokenize_math_question[0]} {operation} {tokenize_math_question[-1]} = {answer}"
            )

            time.sleep(sleep)

        return success_count

    def _click_opperation_button(self, xpath: str):
        """A function to click on the right opperation button

        Args:
            xpath (str): the location of the opperation button
        """
        opperation_button = self.driver.find_element(self.by_xpath, xpath)
        self.driver.execute_script("arguments[0].click();", opperation_button)

    """
    GETTING DATA
    ------------
    """

    def get_addition_data(
        self,
        size: int,
        data_inputs_grooming: callable,
        data_outputs_grooming: callable,
        sleep: float = 0.1,
    ) -> Tuple[list, list]:
        """A function to gather all of the addition data

        Args:
            size (int): How many questions and their answers you want to grab
            data_inputs_grooming (callable): A function to transform our data inputs
            data_outputs_grooming (callable): A function to transform our data outputs
            sleep (float, optional): How long the computer should rest before itterating another step.
                .1 is what most tools like pyautogui use, so I too believe it is a good amount

        Returns:
            Tuple[list,list]:
                data_inputs : a list of all of the inputs. Schema :
                    [
                        [
                            [ input_1, input_2 ]
                        ],
                        [
                            [ input_3, input_4 ]
                        ],
                        ...
                    ]
                data_outputs : a list of all of the outputs. Schema :
                    [
                        [
                            [ output_1 ]
                        ],
                        [
                            [ output_2 ]
                        ],
                        ...
                    ]
        """
        self._click_opperation_button(self.addition_button_xpath)
        return self._collect_data(
            size=size,
            data_inputs_grooming=data_inputs_grooming,
            data_outputs_grooming=data_outputs_grooming,
            sleep=sleep,
        )

    def get_subtraction_data(
        self,
        size: int,
        data_inputs_grooming: callable,
        data_outputs_grooming: callable,
        sleep: float = 0.1,
    ) -> Tuple[list, list]:
        """A function to gather all of the subtraction data

        Args:
            size (int): How many questions and their answers you want to grab
            data_inputs_grooming (callable): A function to transform our data inputs
            data_outputs_grooming (callable): A function to transform our data outputs
            sleep (float, optional): How long the computer should rest before itterating another step.
                .1 is what most tools like pyautogui use, so I too believe it is a good amount

        Returns:
            Tuple[list,list]:
                data_inputs : a list of all of the inputs. Schema :
                    [
                        [
                            [ input_1, input_2 ]
                        ],
                        [
                            [ input_3, input_4 ]
                        ],
                        ...
                    ]
                data_outputs : a list of all of the outputs. Schema :
                    [
                        [
                            [ output_1 ]
                        ],
                        [
                            [ output_2 ]
                        ],
                        ...
                    ]
        """
        self._click_opperation_button(self.subtraction_button_xpath)
        return self._collect_data(
            size=size,
            data_inputs_grooming=data_inputs_grooming,
            data_outputs_grooming=data_outputs_grooming,
            sleep=sleep,
        )

    def get_multiplication_data(
        self,
        size: int,
        data_inputs_grooming: callable,
        data_outputs_grooming: callable,
        sleep: float = 0.1,
    ) -> Tuple[list, list]:
        """A function to gather all of the multiplication data

        Args:
            size (int): How many questions and their answers you want to grab
            data_inputs_grooming (callable): A function to transform our data inputs
            data_outputs_grooming (callable): A function to transform our data outputs
            sleep (float, optional): How long the computer should rest before itterating another step.
                .1 is what most tools like pyautogui use, so I too believe it is a good amount

        Returns:
            Tuple[list,list]:
                data_inputs : a list of all of the inputs. Schema :
                    [
                        [
                            [ input_1, input_2 ]
                        ],
                        [
                            [ input_3, input_4 ]
                        ],
                        ...
                    ]
                data_outputs : a list of all of the outputs. Schema :
                    [
                        [
                            [ output_1 ]
                        ],
                        [
                            [ output_2 ]
                        ],
                        ...
                    ]
        """
        self._click_opperation_button(self.multiplication_button_xpath)
        return self._collect_data(
            size=size,
            data_inputs_grooming=data_inputs_grooming,
            data_outputs_grooming=data_outputs_grooming,
            sleep=sleep,
        )

    def get_division_data(
        self,
        size: int,
        data_inputs_grooming: callable,
        data_outputs_grooming: callable,
        sleep: float = 0.1,
    ) -> Tuple[list, list]:
        """A function to gather all of the division data

        Args:
            size (int): How many questions and their answers you want to grab
            data_inputs_grooming (callable): A function to transform our data inputs
            data_outputs_grooming (callable): A function to transform our data outputs
            sleep (float, optional): How long the computer should rest before itterating another step.
                .1 is what most tools like pyautogui use, so I too believe it is a good amount

        Returns:
            Tuple[list,list]:
                data_inputs : a list of all of the inputs. Schema :
                    [
                        [
                            [ input_1, input_2 ]
                        ],
                        [
                            [ input_3, input_4 ]
                        ],
                        ...
                    ]
                data_outputs : a list of all of the outputs. Schema :
                    [
                        [
                            [ output_1 ]
                        ],
                        [
                            [ output_2 ]
                        ],
                        ...
                    ]
        """
        self._click_opperation_button(self.division_button_xpath)
        return self._collect_data(
            size=size,
            data_inputs_grooming=data_inputs_grooming,
            data_outputs_grooming=data_outputs_grooming,
            sleep=sleep,
        )

    """
    ANSWERING QUESTIONS
    -------------------
    """

    def answer_addition_questions(
        self,
        dnn: DeepNeuralNetwork,
        data_inputs_grooming: callable,
        data_outputs_grooming: callable,
        amount: int,
        sleep: float = 0.1,
    ) -> int:
        """A function to answer the addition math questions on the webpage

        Args:
            dnn (DeepNeuralNetwork): A deep neural network. More info in deep_neural_network.py
            data_inputs_grooming (callable): A function to transform our data inputs
            data_outputs_grooming (callable): A function to transform our data outputs
            round_answer (int): The A in AI stands for artificial, and sometimes there is some handicaps needed.
                This varible will help round to the Nth place
            amount (int): How many questions you want to answer
            sleep (float, optional): How long the computer should rest before itterating another step.
                .1 is what most tools like pyautogui use, so I too believe it is a good amount
        Returns:
            int: the amount of successfully answered questions
        """
        self._click_opperation_button(self.addition_button_xpath)
        return self._answer_questions(
            dnn=dnn,
            data_inputs_grooming=data_inputs_grooming,
            data_outputs_grooming=data_outputs_grooming,
            round_answer=0,
            amount=amount,
            operation="+",
            sleep=sleep,
        )

    def answer_subtraction_questions(
        self,
        dnn: DeepNeuralNetwork,
        data_inputs_grooming: callable,
        data_outputs_grooming: callable,
        amount: int,
        sleep: float = 0.1,
    ) -> int:
        """A function to answer the subtraction math questions on the webpage

        Args:
            dnn (DeepNeuralNetwork): A deep neural network. More info in deep_neural_network.py
            data_inputs_grooming (callable): A function to transform our data inputs
            data_outputs_grooming (callable): A function to transform our data outputs
            round_answer (int): The A in AI stands for artificial, and sometimes there is some handicaps needed.
                This varible will help round to the Nth place
            amount (int): How many questions you want to answer
            sleep (float, optional): How long the computer should rest before itterating another step.
                .1 is what most tools like pyautogui use, so I too believe it is a good amount
        Returns:
            int: the amount of successfully answered questions
        """
        self._click_opperation_button(self.subtraction_button_xpath)
        return self._answer_questions(
            dnn=dnn,
            data_inputs_grooming=data_inputs_grooming,
            data_outputs_grooming=data_outputs_grooming,
            round_answer=0,
            amount=amount,
            operation="-",
            sleep=sleep,
        )

    def answer_multiplication_questions(
        self,
        dnn: DeepNeuralNetwork,
        data_inputs_grooming: callable,
        data_outputs_grooming: callable,
        amount: int,
        sleep: float = 0.1,
    ) -> int:
        """A function to answer the multiplication math questions on the webpage

        Args:
            dnn (DeepNeuralNetwork): A deep neural network. More info in deep_neural_network.py
            data_inputs_grooming (callable): A function to transform our data inputs
            data_outputs_grooming (callable): A function to transform our data outputs
            round_answer (int): The A in AI stands for artificial, and sometimes there is some handicaps needed.
                This varible will help round to the Nth place
            amount (int): How many questions you want to answer
            sleep (float, optional): How long the computer should rest before itterating another step.
                .1 is what most tools like pyautogui use, so I too believe it is a good amount
        Returns:
            int: the amount of successfully answered questions
        """
        self._click_opperation_button(self.multiplication_button_xpath)
        return self._answer_questions(
            dnn=dnn,
            data_inputs_grooming=data_inputs_grooming,
            data_outputs_grooming=data_outputs_grooming,
            round_answer=0,
            amount=amount,
            operation="*",
            sleep=sleep,
        )

    def answer_division_questions(
        self,
        dnn: DeepNeuralNetwork,
        data_inputs_grooming: callable,
        data_outputs_grooming: callable,
        amount: int,
        sleep: float = 0.1,
    ) -> int:
        """A function to answer the division math questions on the webpage

        Args:
            dnn (DeepNeuralNetwork): A deep neural network. More info in deep_neural_network.py
            data_inputs_grooming (callable): A function to transform our data inputs
            data_outputs_grooming (callable): A function to transform our data outputs
            round_answer (int): The A in AI stands for artificial, and sometimes there is some handicaps needed.
                This varible will help round to the Nth place
            amount (int): How many questions you want to answer
            sleep (float, optional): How long the computer should rest before itterating another step.
                .1 is what most tools like pyautogui use, so I too believe it is a good amount
        Returns:
            int: the amount of successfully answered questions
        """
        self._click_opperation_button(self.division_button_xpath)
        return self._answer_questions(
            dnn=dnn,
            data_inputs_grooming=data_inputs_grooming,
            data_outputs_grooming=data_outputs_grooming,
            round_answer=2,
            amount=amount,
            operation="/",
            sleep=sleep,
        )
