import tkinter as tk
from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import Conv2D, Dense, Flatten, MaxPool2D, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ReduceLROnPlateau, ModelCheckpoint
import os
import numpy as np

checkpoint_path = "training/cp.ckpt"
model = Sequential()
model.add(Conv2D(filters = 8, kernel_size = (5,5),padding = 'Same', 
                 activation ='relu', input_shape = (28,28,1)))
model.add(MaxPool2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Conv2D(filters = 16, kernel_size = (3,3),padding = 'Same', 
                 activation ='relu'))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))
model.add(Dropout(0.25))
# fully connected
model.add(Flatten())
model.add(Dense(256, activation = "relu"))
model.add(Dropout(0.5))
model.add(Dense(10, activation = "softmax"))
model.load_weights(checkpoint_path)

size_of_board = 560
rows = 28
cols = rows

mode_to_board = {
    "draw":['black',255],
    "erase":['white',0],
}

class AI_Number_Guesser:
    def __init__(self):
        # // -- Initalizing Varibles that will be used later -- //
        # options : draw erase start end
        self.mode = "draw"
        # 4 states : empty, wall, start, end
        self.board = []
        # These values come up all the time and instead of waisting computing power im going to init them
        self.row_spacing = int(size_of_board / rows)
        self.column_spacing = int(size_of_board / cols)

        # // -- Initalizing the window -- //
        self.window = tk.Tk()
        self.window.title("Number Guesser V1.0")

        # // -- Initalizing the top frame -- //
        # Creating the top frame
        self.top_frame = tk.LabelFrame(self.window,bg="gray")
        self.top_frame.pack(fill="both", expand="yes")
        # Creating the Mode Label
        self.mode_label = tk.Label(self.top_frame,text = f"Mode : {self.mode}",bg="gray")
        self.mode_label.pack(side=tk.LEFT)
        # Creating the draw mode button
        self.draw_mode_btn = tk.Button(self.top_frame,text='draw',command=self.draw_mode,bg="gray")
        self.draw_mode_btn.pack(side=tk.LEFT)
        # Creating the erase mode button
        self.erase_mode_btn = tk.Button(self.top_frame,text='erase',command=self.erase_mode,bg="gray")
        self.erase_mode_btn.pack(side=tk.LEFT)

        # // -- Initalizing the canvas -- //
        self.canvas = tk.Canvas(self.window, width=size_of_board, height=size_of_board)
        # Binding click and move to the canvas
        self.canvas.bind("<Button-1>",self.edit_tiles)
        self.canvas.bind("<B1-Motion>",self.edit_tiles)
        self.canvas.pack()

        # // -- Initalizing the Bottom frame -- //
        # Creating the bottom frame
        self.bottom_frame = tk.LabelFrame(self.window,bg="gray")
        self.bottom_frame.pack(fill="both", expand="yes")
        # Creating the clear button
        self.clear_btn = tk.Button(self.bottom_frame,text='clear',command=self.initialize_board,bg="gray")
        self.clear_btn.pack(side=tk.LEFT)

        self.AI_GUESS = tk.StringVar(self.bottom_frame)
        self.AI_GUESS_label = tk.Label(self.bottom_frame, textvariable=self.AI_GUESS)
        self.AI_GUESS_label.pack(side=tk.LEFT)
        self.AI_GUESS.set("The Number You Drew Is : ")

        # Initalizing the board on init of the class
        self.initialize_board()
    
    def edit_tiles(self,event):
        # If we are within the regins of the canvas
        # I use a not to the logic because I dont want to work with overly indented code
        if not (
            (event.x >= 0) and 
            (event.x < size_of_board) and 
            (event.y >= 0) and 
            (event.y < size_of_board)
            ): return
        # Using the dictionary at the top to be able to made the drawl compact
        self.canvas.create_rectangle(
            int(event.x/self.row_spacing)*self.row_spacing,
            int(event.y/self.column_spacing)*self.column_spacing,
            int(event.x/self.row_spacing)*self.row_spacing+self.row_spacing,  
            int(event.y/self.column_spacing)*self.column_spacing+self.column_spacing,
            fill = mode_to_board[self.mode][0])
        # update the board
        self.board[int(event.y/self.column_spacing)][int(event.x/self.row_spacing)] = mode_to_board[self.mode][1]
        ai_board = np.array(self.board)
        ai_board = ai_board.reshape((-1, 28, 28, 1))
        pre = model.predict(ai_board)[0]
        self.AI_GUESS.set(f"The Number You Drew Is : {np.argmax(pre, axis=0)}")

    # The loop to make the screen run
    def mainloop(self):
        while True:
            self.window.update()

    def initialize_board(self):
        # // -- creating the board -- //
        # we can not create the board by saying [[0]*row]*col because python will pointer all list
        self.board = []
        for y in range(rows):
            self.board.append([])
            for _ in range(cols):
                self.board[y].append(0)
        # clearing the canvas
        self.canvas.delete("all")

        # Drawling a line where the rows are
        for i in range(rows):
            self.canvas.create_line(
                i * self.row_spacing, 0, i * self.row_spacing, size_of_board,
            )
        # Drawling a line where the columns are
        for i in range(cols):
            self.canvas.create_line(
                0, i * self.column_spacing, size_of_board, i * self.column_spacing,
            )     
    
    def draw_mode(self):
        self.mode = "draw"
        self.mode_label.config(text=f"Mode : {self.mode}")
    def erase_mode(self):
        self.mode = "erase"
        self.mode_label.config(text=f"Mode : {self.mode}")


AI = AI_Number_Guesser ()
AI.mainloop()