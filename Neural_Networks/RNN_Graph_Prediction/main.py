import tkinter as tk
from tkinter import font

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from recursive_neural_network import (
    RecursiveNeuralNetwork,
    LEAKY_RELU,
    get_training_in_out,
)


class GraphAI(tk.Tk):
    def __init__(self, rnn: RecursiveNeuralNetwork, reference_size: int = 20):
        super().__init__()

        self.rnn = rnn
        self.reference_size = reference_size
        self.background = "#333"
        self.y_list = []

        self.title("Graph AI")
        self.config(background=self.background)

        self.font_large = font.Font(size=self.reference_size * 2)
        self.font_med = font.Font(size=self.reference_size)
        self.font_small = font.Font(size=self.reference_size // 2)

        """
        RESET BUTTON
        Y : [   ] SUBMIT BUTTON
        ---------------------------------
        Graph
        """

        # FRAMES
        # ------
        self.graph_input_frame = tk.Frame(
            master=self,
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            relief=tk.SOLID,
            background=self.background,
        )

        self.graph_frame = tk.Frame(
            master=self,
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            relief=tk.SOLID,
            background=self.background,
        )

        self.graph_input_frame.grid(column=0, row=0)
        self.graph_frame.grid(column=0, row=1)

        # GRAPH INPUT FRAME
        # -----------------

        self.reset_button = tk.Button(
            master=self.graph_input_frame,
            text="Reset Graph",
            font=self.font_med,
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            command=self.reset_graph,
        )

        self.coordinate_label = tk.Label(
            master=self.graph_input_frame,
            text="Please Enter Y Coordinate :",
            font=self.font_med,
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            background=self.background,
        )

        self.coordinate_entry = tk.Entry(
            master=self.graph_input_frame,
            font=self.font_large,
            width=self.reference_size // 4,
        )

        self.coordinate_button = tk.Button(
            master=self.graph_input_frame,
            text="Submit Point",
            font=self.font_med,
            padx=self.reference_size,
            pady=self.reference_size // 2,
            command=self.add_coordinate,
        )

        self.reset_button.grid(column=0, row=0, sticky="nsw")

        self.coordinate_label.grid(column=0, row=1, sticky="nsw")
        self.coordinate_entry.grid(column=1, row=1)
        self.coordinate_button.grid(column=2, row=1, sticky="w")

        # GRAPH FRAME
        # -----------

        self.graph_figure = Figure(
            figsize=(self.reference_size // 4, self.reference_size // 4),
            dpi=self.reference_size * 5,
        )
        self.subplot = self.graph_figure.add_subplot(111)
        self.graph_canvas = FigureCanvasTkAgg(
            master=self.graph_frame, figure=self.graph_figure
        )

        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack()

    def add_coordinate(self):
        point = str(self.coordinate_entry.get())

        self.coordinate_entry.delete(0, tk.END)

        try:
            self.y_list.append(float(point))
        except:
            return

        # Clear existing graph
        self.subplot.clear()

        if len(self.y_list) > (self.rnn.input_size + 1):
            rnn.reset()
            max_y = max(self.y_list)
            min_y = min(self.y_list)
            train_in, train_out = get_training_in_out(
                data=(np.array(self.y_list) - min_y) / (max_y - min_y),
                input_size=self.rnn.input_size,
                step_size=1,
            )
            for _ in range(100):
                self.rnn.train(
                    training_inputs=train_in, training_outputs=train_out, step_size=1
                )

            ai_predictions = self.rnn.predict_full(inputs=train_out[-1], step_size=10)
            self.subplot.plot(
                np.append(self.y_list, (ai_predictions * (max_y - min_y)) + min_y),
                label="AI",
            )

        # Plot updated data on the graph
        self.subplot.plot(self.y_list, label="Given")

        # Set labels and legend
        self.subplot.set_xlabel("X-axis")
        self.subplot.set_ylabel("Y-axis")
        self.subplot.legend()

        # Redraw the graph canvas
        self.graph_canvas.draw()

        self.update()

    def reset_graph(self):
        self.y_list = []
        self.subplot.clear()
        self.graph_canvas.draw()

        self.update()

def main():
    rnn = RecursiveNeuralNetwork(input_size=8, activation_function=LEAKY_RELU, seed=1)
    graph_ai = GraphAI(rnn=rnn)
    graph_ai.mainloop()

if __name__ == "__main__":
    main()