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
        data_inputs_grooming: dict,
        data_outputs_grooming: dict,
        sleep: float = 0.1,
    ) -> Tuple[list, list]:
        """A function to grab the questions and their answers for a math question

        Args:
            size (int): How many questions and their answers you want to grab
            data_inputs_grooming (dict): Schema
            {
                "addition_bias": int, # the number you want added to the data_input values
                "multiplication_bias": float, # the number you want multiplied to the data_input values
            }
                formula :
                    ( data_input + addition_bias ) * multiplication_bias
            data_outputs_grooming (dict): Schema
            {
                "addition_bias": int, # the number you want added to the data_output values
                "multiplication_bias": float, # the number you want multiplied to the data_output values
            }
                formula :
                    ( data_output + addition_bias ) * multiplication_bias

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
            math_question = self.driver.find_element(
                self.by_xpath, self.math_question_xpath
            )
            tokenize_math_question = math_question.text.split(" ")

            text_box = self.driver.find_element(
                self.by_xpath, self.answer_text_box_xpath
            )
            text_box.send_keys("-100")

            submit_button = self.driver.find_element(
                self.by_xpath, self.submit_button_xpath
            )
            self.driver.execute_script("arguments[0].click();", submit_button)

            answer_response = self.driver.find_element(
                self.by_xpath, self.answer_response_xpath
            )

            # adding the fields to input
            data_inputs.append(
                [
                    [
                        float(
                            int(tokenize_math_question[0])
                            + data_inputs_grooming["addition_bias"]
                        )
                        * data_inputs_grooming["multiplication_bias"],
                        float(
                            int(tokenize_math_question[-1])
                            + data_inputs_grooming["addition_bias"]
                        )
                        * data_inputs_grooming["multiplication_bias"],
                    ]
                ]
            )
            data_outputs.append(
                [
                    [
                        float(
                            int(answer_response.text.split(" ")[-1][:-1])
                            + data_outputs_grooming["addition_bias"]
                        )
                        * data_outputs_grooming["multiplication_bias"],
                    ]
                ]
            )
            time.sleep(sleep)

        return data_inputs, data_outputs

    def _answer_questions(
        self,
        dnn: DeepNeuralNetwork,
        data_inputs_grooming: dict,
        data_outputs_grooming: dict,
        round_answer:int,
        amount: int,
        operation: str,
        sleep: float = 0.1,
    ) -> int:
        success_count = 0
        for _ in range(amount):
            math_question = self.driver.find_element(
                self.by_xpath, self.math_question_xpath
            )
            tokenize_math_question = math_question.text.split(" ")

            answer = (
                dnn.forward_propagation(
                    input_data=np.array(
                        [
                            [
                                (
                                    int(tokenize_math_question[0])
                                    + data_inputs_grooming["addition_bias"]
                                )
                                * data_inputs_grooming["multiplication_bias"],
                                (
                                    int(tokenize_math_question[-1])
                                    + data_inputs_grooming["addition_bias"]
                                )
                                * data_inputs_grooming["multiplication_bias"],
                            ]
                        ]
                    )
                )[0][0]
                * data_outputs_grooming["multiplication_bias"]
                + data_outputs_grooming["addition_bias"]
            )

            answer = round(answer,ndigits=round_answer)

            text_box = self.driver.find_element(
                self.by_xpath, self.answer_text_box_xpath
            )
            text_box.send_keys(answer)

            submit_button = self.driver.find_element(
                self.by_xpath, self.submit_button_xpath
            )
            self.driver.execute_script("arguments[0].click();", submit_button)

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
        opperation_button = self.driver.find_element(self.by_xpath, xpath)
        self.driver.execute_script("arguments[0].click();", opperation_button)

    """
    GETTING DATA
    ------------
    """

    def get_addition_data(
        self,
        size: int,
        data_inputs_grooming: dict,
        data_outputs_grooming: dict,
        sleep: float = 0.1,
    ):
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
        data_inputs_grooming: dict,
        data_outputs_grooming: dict,
        sleep: float = 0.1,
    ):
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
        data_inputs_grooming: dict,
        data_outputs_grooming: dict,
        sleep: float = 0.1,
    ):
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
        data_inputs_grooming: dict,
        data_outputs_grooming: dict,
        sleep: float = 0.1,
    ):
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
        data_inputs_grooming: dict,
        data_outputs_grooming: dict,
        amount: int,
        sleep: float = 0.1,
    ):
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
        data_inputs_grooming: dict,
        data_outputs_grooming: dict,
        amount: int,
        sleep: float = 0.1,
    ):
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
        data_inputs_grooming: dict,
        data_outputs_grooming: dict,
        amount: int,
        sleep: float = 0.1,
    ):
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
        data_inputs_grooming: dict,
        data_outputs_grooming: dict,
        amount: int,
        sleep: float = 0.1,
    ):
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
