import csv
import statistics
import tkinter as tk
from tkinter import font
from typing import List

import numpy as np

from random_forest import RandomForest
from utils import read_csv_file


class WebDT(tk.Tk):
    def __init__(
        self,
        random_forest: RandomForest,
        dataset_headers: List[str],
        dataset_diagnoses: List[str],
        reference_size: int = 20,
    ):
        super().__init__()

        self.random_forest = random_forest
        self.dataset_headers = dataset_headers
        self.dataset_diagnoses = dataset_diagnoses
        self.current_diagonses = [0] * len(self.dataset_headers)

        self.reference_size = reference_size
        self.white_background = "#F0F0F0"

        self.title("WebDT NOT REAL MEDICAL ADVICE")
        self.config(background=self.white_background)
        self.font_large = font.Font(size=self.reference_size * 4)
        self.font_med = font.Font(size=self.reference_size * 2)
        self.font_small = font.Font(size=self.reference_size // 2)
        """
            You have common symptoms with...
                    DEATH!
        breakdown
        ------------------------------------
        select your symptoms : 
        * A    * D    * G  ...
        * B    * E    * H  ...
        * C    * F    * I  ...
        """

        # FRAMES
        # ------
        self.diagnose_frame = tk.Frame(
            master=self,
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            relief=tk.SOLID,
            background=self.white_background,
        )
        self.break_down_label = tk.Label(
            master=self,
            text="Break Down :\n100% Healthy",
            font=self.font_small,
            background=self.white_background,
            foreground="red",
            anchor="nw",
            justify="left"
        )
        self.select_your_symptoms_label = tk.Label(
            master=self,
            text="Select your symptoms :",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=self.font_med,
            background=self.white_background,
            foreground="black",
        )
        self.symptoms_frame = tk.Frame(
            master=self,
            padx=self.reference_size,
            pady=self.reference_size,
            relief=tk.SOLID,
            background=self.white_background,
        )
        self.not_medical_advice = tk.Label(
            master=self,
            text="Please DO NOT use this as medical advice, this was created for entertainment purposes only. If you are feeling anything abnormal it is best to consult with a medical professional. I reserve no rights or liablity if this is used in serious practice... don't listen to people on the internet!",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=self.font_small,
            background=self.white_background,
            foreground="black",
        )

        self.diagnose_frame.grid(column=0, row=0, sticky="ns")
        self.break_down_label.grid(column=0, row=1, sticky="nsw")
        self.select_your_symptoms_label.grid(column=0, row=2, sticky="nsw")
        self.symptoms_frame.grid(column=0, row=3, sticky="nsew")
        self.not_medical_advice.grid(column=0,row=4,sticky="nsew")

        # DIAGNOSE FRAME
        # --------------

        self.you_have_label = tk.Label(
            master=self.diagnose_frame,
            text="You have common symptoms with...",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=self.font_med,
            background=self.white_background,
            foreground="black",
        )
        self.diagnoses_label = tk.Label(
            master=self.diagnose_frame,
            text="Healthy",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=self.font_large,
            background=self.white_background,
            foreground="red",
        )

        self.you_have_label.grid(column=0, row=0)
        self.diagnoses_label.grid(column=0, row=1)

        # SYMPTOMS FRAME
        # --------------

        self.header_buttons: List[tk.Button] = []
        self.button_grid = 15
        for header_index, header in enumerate(self.dataset_headers):

            def symptom_selected_closure(index: int)->callable:
                """A function to de-reference the value header_index, so buttons can work uniquely

                Args:
                    index (int): header_index

                Returns:
                    callable: the lambda function tied to the symptom_selected
                """
                return lambda: self.symptom_selected(index=index)

            _header_button = tk.Radiobutton(
                master=self.symptoms_frame,
                text=header,
                font=self.font_small,
                background=self.white_background,
                foreground="black",
                command=symptom_selected_closure(index=header_index),
            )
            _header_button.grid(
                column=header_index // self.button_grid,
                row=header_index % self.button_grid,
                sticky="nsw",
            )
            self.header_buttons.append(_header_button)

    def symptom_selected(self, index: int):
        """A function to toggle a symptom and predict the users health

        Args:
            index (int): an index of the button (and also the current_diagonses symptiom)
        """

        # checking what the value currently is
        current_status = self.current_diagonses[index]

        # if the value is 1 (toggled on) we want to toggle it off, else we do the inverse
        if current_status:
            self.current_diagonses[index] = 0
            self.header_buttons[index].config(
                background=self.white_background, foreground="black"
            )
        else:
            self.current_diagonses[index] = 1
            self.header_buttons[index].config(
                background="green", foreground=self.white_background
            )

        
        # Predicting what the user may have
        # WARNING - I am not a licened doctor and this is only for entertainment purposes.
        # Please do not consult this app as medical advice.
        _, predictions =self.random_forest.make_prediction(np.array(self.current_diagonses))
        
        breakdown_dict = {prediction: (predictions.count(prediction)/len(predictions))*100 for prediction in set(predictions)}
        breakdown_str = "Break Down :\n"
        index = 0

        # Showing all of the predictions to the user
        for prediction, prediction_chance in breakdown_dict.items():
            breakdown_str += f'   {self.dataset_diagnoses[int(prediction)]} {prediction_chance}%'
            index += 1
            if not(index%5):breakdown_str+="\n"

        # Some additional logic to help the random forest, if the user is only 50% healthy, than we display what the illness may be
        if breakdown_dict.get(0,0) <= 50:
            while 0 in predictions:
                predictions.remove(0)
            illness = statistics.mode(predictions)
        else:
            illness = 0

        # Updating the labels with the new predicted information
        self.diagnoses_label.config(text=self.dataset_diagnoses[int(illness)])
        self.break_down_label.config(text=breakdown_str)

        self.update()

def main():
    # WARNING - I am not a licened doctor and this is only for entertainment purposes.
    # Please do not consult this app as medical advice. Dataset can be found here :
    # https://www.kaggle.com/datasets/kaushil268/disease-prediction-using-machine-learning
    diseases_csv = read_csv_file("DiseaseSymptoms.csv")
    diseases_csv_headers = diseases_csv[0]
    diseases_csv_body = diseases_csv[1:]
    np_diseases_csv = np.array(diseases_csv_body)[:, :-1].astype(int)

    # A depth of 25 was chosen because we have 43 rows in our csv. This means that at very least we would need 43 / 2 of a depth to capture all possible outputs
    # 42 for obvious reasons~
    non_medically_licensed_doctor = RandomForest(
        dataset=np_diseases_csv,
        tree_count=42,
        min_split_length=2,
        max_depth=25,
        require_variance_reduction_greater_than_0=True,
        seed=1,
    )

    # if you want to see what the different trees look like, comment this out
    # non_medically_licensed_doctor.print_forest()

    web_dt = WebDT(
        random_forest=non_medically_licensed_doctor,
        dataset_headers=diseases_csv_headers[:-2],
        dataset_diagnoses=np.array(diseases_csv_body)[:, -1],
    )
    web_dt.mainloop()

if __name__ == "__main__":
    main()