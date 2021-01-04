from tkinter import *
import random
import time
import numpy as np
from PIL import ImageTk,Image

# Define useful parameters
size_of_board = 600
rows = 10
cols = int(rows)
DELAY = 25
snake_initial_length = 3
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 2
RED_COLOR = "#EE4035"
BLUE_COLOR = "#0492CF"
Green_color = "#7BC043"

BLUE_COLOR_LIGHT = '#67B0CF'
RED_COLOR_LIGHT = '#EE7E77'

'''
This is code that I wrote to attach to the snake game.
What this code does is with an even height, will return a hamiltonian path
to the board. There is a simple pattern that can be followed that looks as such
0   1   2   3 ...   1W-1
   2W-2 ...  W+2 W+1 W
   2W-1 2W 2W+1 ... 3W-3
   ...
(h-1)(W) ...       NW-N
from there the left hand side will then jut up. 

A graph of how this will look is :
4x4
0  1  2  3
15 6  5  4
14 7  8  9
13 12 11 10

This graph is important because it will be the generic perfect play path to take.
However this graph is not optimal in speed in it's current stat, which is why
there is an advance pathing algorithm that is found later. 
'''
def build_path(width,height):
    '''
    Parameters
    ----------
    width : The Width of the board.
    height : The Height of the board.

    Returns
    -------
    path : A hamiltonian path that the AI will use to know it's next move.
    '''
    # creating a 2 diminsional arry of all 0s
    path = [ [0 for _ in range(width) ] for _ in range(height) ]
    # the fisrt row will always be 0 -> N-1. All of the others don't follow this pattern
    for node in range(width) : path[0][node] = node
    # creating an index counter because it will be easier increment a varible per itteration, than apply more logic
    index = width
    # for the length of the height - 2, and skip 2. 
    # we are skipping 2 because in 1 itteration we will go back and forth covering 2 rows
    for row in range(1,height-2,2):
        # This loop fills right to left, stoping at the path[n][0] index, leaving it still 0
        for node in range(width-1) :
            path[row][-( 1 + node )] = index
            index += 1
        # This loop fills left to right, stoping at the path[n][w] index, leaving path[n][0] still 0
        for node in range(1,width) :
            path[row + 1][node] = index
            index += 1
    # this loop fill the bottom row. This fills right to left and leaves no 0s
    for node in range(width-1):
        path[-1][-( 1 + node )] = index
        index += 1
    # this last loop fills the 0 index of all lists from bottom to top, and stops at path[0][0]
    for node in range(height-1):
        path[-( 1 + node )][0] = index
        index += 1
    # returning the hamiltonian path we created
    return path

class SnakeAndApple:
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.ai_path = build_path(rows,cols)
        self.window = Tk()
        self.window.title("Snake-and-Apple-WithAI")
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        # Input from user in form of clicks and keyboard
        self.window.bind("<Key>", self.key_input)
        self.window.bind("<Button-1>", self.mouse_input)
        self.play_again()
        self.begin = False    

    def initialize_board(self):
        self.board = []
        self.apple_obj = []
        self.old_apple_cell = []
        
        row_spacing = size_of_board / rows
        column_spacing = size_of_board / cols

        for i in range(rows):
            for j in range(cols):
                self.board.append((i, j))

        for i in range(rows):
            self.canvas.create_line(
                i * row_spacing, 0, i * row_spacing, size_of_board,
            )

        for i in range(cols):
            self.canvas.create_line(
                0, i * column_spacing, size_of_board, i * column_spacing,
            )
        
        '''
        -----
        This section of code can be uncommented, its purpose it to show the 
        hamiltonian path if you want to see how it looks
        -----
        
        r_index = 1
        elm_index = 1
        for r in self.ai_path:
            elm_index = 1
            for elm in r:
                self.canvas.create_text(
                    (elm_index) * row_spacing - row_spacing/2,
                    (r_index) * column_spacing - column_spacing/2,
                    font="cmr 11 bold",
                    fill=RED_COLOR,
                    text=elm
                    )
                elm_index += 1
            r_index += 1
        '''
        
    def initialize_snake(self):
        self.snake = []
        self.ai_on = False
        self.crashed = False
        self.snake_heading = "Right"
        self.last_key = self.snake_heading
        self.forbidden_actions = {}
        self.forbidden_actions["Right"] = "Left"
        self.forbidden_actions["Left"] = "Right"
        self.forbidden_actions["Up"] = "Down"
        self.forbidden_actions["Down"] = "Up"
        self.snake_objects = []
        for i in range(snake_initial_length):
            self.snake.append((i, 0))

    def play_again(self):
        self.canvas.delete("all")
        self.initialize_board()
        self.initialize_snake()
        self.place_apple()
        self.display_snake(mode="complete")
        self.begin_time = time.time()

    def mainloop(self):
        while True:
            self.window.update()
            if self.begin:
                if not self.crashed:
                    self.window.after(DELAY, self.update_snake(self.last_key))
                else:
                    self.begin = False
                    self.display_gameover()

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------
    def display_gameover(self):
        score = len(self.snake)
        self.canvas.delete("all")
        score_text = "Scores \n"

        # put gif image on canvas
        # pic's upper left corner (NW) on the canvas is at x=50 y=10

        self.canvas.create_text(
            size_of_board / 2,
            3 * size_of_board / 8,
            font="cmr 40 bold",
            fill=Green_color,
            text=score_text,
        )
        score_text = str(score)
        self.canvas.create_text(
            size_of_board / 2,
            1 * size_of_board / 2,
            font="cmr 50 bold",
            fill=BLUE_COLOR,
            text=score_text,
        )
        time_spent = str(np.round(time.time() - self.begin_time, 1)) + 'sec'
        self.canvas.create_text(
            size_of_board / 2,
            3 * size_of_board / 4,
            font="cmr 20 bold",
            fill=BLUE_COLOR,
            text=time_spent,
        )
        score_text = "Click to play again \n"
        self.canvas.create_text(
            size_of_board / 2,
            15 * size_of_board / 16,
            font="cmr 20 bold",
            fill="gray",
            text=score_text,
        )

    def place_apple(self):
        # Place apple randomly anywhere except at the cells occupied by snake
        unoccupied_cels = set(self.board) - set(self.snake)
        self.apple_cell = random.choice(list(unoccupied_cels))
        row_h = int(size_of_board / rows)
        col_w = int(size_of_board / cols)
        x1 = self.apple_cell[0] * row_h
        y1 = self.apple_cell[1] * col_w
        x2 = x1 + row_h
        y2 = y1 + col_w
        self.apple_obj = self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=RED_COLOR_LIGHT, outline=BLUE_COLOR,
        )

    def display_snake(self, mode=""):
        # Remove tail from display if it exists
        if self.snake_objects != []:
            self.canvas.delete(self.snake_objects.pop(0))
        
        if mode == "complete":
            for i, cell in enumerate(self.snake):
                # print(cell)
                row_h = int(size_of_board / rows)
                col_w = int(size_of_board / cols)
                x1 = cell[0] * row_h
                y1 = cell[1] * col_w
                x2 = x1 + row_h
                y2 = y1 + col_w
                self.snake_objects.append(
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=BLUE_COLOR, outline=BLUE_COLOR,
                    )
                )
                
        else:
            # only update head
            cell = self.snake[-1]
            row_h = int(size_of_board / rows)
            col_w = int(size_of_board / cols)
            x1 = cell[0] * row_h
            y1 = cell[1] * col_w
            x2 = x1 + row_h
            y2 = y1 + col_w
            self.snake_objects.append(
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=BLUE_COLOR, outline=RED_COLOR,
                )
            )
            if self.snake[0] == self.old_apple_cell:
                self.snake.insert(0, self.old_apple_cell)
                self.old_apple_cell = []
                tail = self.snake[0]
                row_h = int(size_of_board / rows)
                col_w = int(size_of_board / cols)
                x1 = tail[0] * row_h
                y1 = tail[1] * col_w
                x2 = x1 + row_h
                y2 = y1 + col_w
                self.snake_objects.insert(
                    0,
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=BLUE_COLOR, outline=RED_COLOR
                    ),
                )
            self.window.update()

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------
    def update_snake(self, key):
        if self.ai_on:
            key = self.ai_input()
            
        
        # Check if it hit the wall or its own body
        tail = self.snake[0]
        head = self.snake[-1]
        if tail != self.old_apple_cell:
            self.snake.pop(0)
        if key == "Left":
            self.snake.append((head[0] - 1, head[1]))
        elif key == "Right":
            self.snake.append((head[0] + 1, head[1]))
        elif key == "Up":
            self.snake.append((head[0], head[1] - 1))
        elif key == "Down":
            self.snake.append((head[0], head[1] + 1))

        head = self.snake[-1]
        if (
                head[0] > cols - 1
                or head[0] < 0
                or head[1] > rows - 1
                or head[1] < 0
                or len(set(self.snake)) != len(self.snake)
        ):
            # Hit the wall / Hit on body
            self.crashed = True
        elif self.apple_cell == head:
            # Got the apple
            self.old_apple_cell = self.apple_cell
            self.canvas.delete(self.apple_obj)
            self.place_apple()
            self.display_snake()
        else:
            self.snake_heading = key
            self.display_snake()
    
    def check_if_key_valid(self, key):
        valid_keys = ["Up", "Down", "Left", "Right"]
        if key in valid_keys and self.forbidden_actions[self.snake_heading] != key:
            return True
        else:
            return False
    
    def mouse_input(self, event):
        self.play_again()
    
    def ai_input(self):
        '''
        Returns
        -------
        return STR which indicates what move the snake ought to take :
            UP DOWN LEFT RIGHT
        '''
        
        # initializing varibles the in's are all in reference to which row the item is in
        head_in = 0
        move_in = 0
        s_move_in = 0
        s_head_in = 0
        
        # A function that is called after every normal move
        def head_inc():
            '''
            Purpose
            -------
            will increment the location of the head by 1. The location of the head
            will be a token to the path array. If the head is at 25, then  
            wherever 25 is on the path, that is the assumed location of the head.
            
            also this function will manage the length of the snake,
            when taking all of the skipping it has been doing into consideration
            '''
            # increments the hdead
            self.head_place += 1
            # if the head of the snake is at the max, reset the head back to 0
            if self.head_place == rows*cols: self.head_place = 0
            # if the skip_turn array is not empty
            if len(self.skip_turn) != 0:
                # for index in the length of the skip_turn array, increment every element by 1
                for i in range(len(self.skip_turn)):
                    self.skip_turn[i] += 1
                # if the last element of the skip_turn array is equal to the snakes length
                # then that element will get removed as well as the length that it added
                if self.skip_turn[-1] >= len(self.snake):
                    self.skip_turn.pop()
                    self.skip_snake_len.pop()
        
        # getting the next number after the number assigned to the heads position.
        # if the number of the head is at the max then to have the next move be 0
        nex_move = self.head_place+1 if self.head_place != rows*cols-1 else 0
        # getting the number key that the apple is in. 
        # This key will be used to find the apples place on the ai's path
        smart_move_address = self.ai_path[self.apple_cell[1]][self.apple_cell[0]]
       
        # A for loop to get the row the head is in.
        for i in self.ai_path:
            if self.head_place in i: break
            s_head_in += 1
        # A for loop to get the row the apple is in.
        for i in self.ai_path:
            if smart_move_address in i: break
            s_move_in += 1
        
        # getting the collum / index that the head is in, in the row
        s_move_loc = self.ai_path[s_move_in].index(smart_move_address)
        # getting the collum / index that the apple is in, in the row
        s_head_loc = self.ai_path[s_head_in].index(self.head_place)
        
        # if the head is not at the top left corner or bottom row.
        # top left corner is because these will only return down, 
        # and we can not have a snake go down on itself
        # bottom row, because going down will cause it to crash into a wall
        if (s_head_loc != 0 )and (s_head_in != rows-1):
            # The new head is 1 row below the current head. This get's the key
            new_head = int(self.ai_path[s_head_in+1][s_head_loc])
            # Taking the delta between the old and new head to know how much was skipped
            new_gain = new_head-int(self.head_place)-1
            
            # if in the even row
            if ((s_move_in % 2 == 0) and 
                # and the apple is ahead the head in the collumn or is on the far left side
                ((s_head_loc <= s_move_loc) or (s_move_loc == 0)) and 
                # if the head and apple are not in the same row
                (s_head_in != s_move_in) and 
                # if the snake has enough tiles avaible to make a move without crashing into itself
                ((sum(self.skip_snake_len) + new_gain + len(self.snake)) < (rows*cols))):
                # the head is set to the key of being 1 down
                self.head_place = int(self.ai_path[s_head_in+1][s_head_loc])
                # the snake len is increased by the amount skipped
                self.skip_snake_len.insert(0,new_gain)
                # the parallel list is given its counter starting at 0
                self.skip_turn.insert(0,0)
                # returns the move down
                return "Down"
            # if in an odd row
            elif ((s_move_in % 2 == 1) and 
                  # and the apple is behind the head in collumn
                  (s_head_loc >= s_move_loc) and 
                  # if the head and apple are not in the same row
                  (s_head_in != s_move_in) and 
                  # if the snake has enough tiles avaible to make a move without crashing into itself
                  ((sum(self.skip_snake_len) + new_gain +  len(self.snake)) < (rows*cols))):
                # the head is set to the key of being 1 down
                self.head_place = int(self.ai_path[s_head_in+1][s_head_loc])
                # the snake len is increased by the amount skipped
                self.skip_snake_len.insert(0,new_gain)
                # the parallel list is given its counter starting at 0
                self.skip_turn.insert(0,0)
                # returns the move down
                return "Down"
        
        # A for loop to get the row the head is in.
        # yes, this is redundent since we already did it with s_head_in; however,
        # mentally it is easier for me to know what is going on
        for i in self.ai_path:
            if self.head_place in i: break
            head_in += 1
         # A for loop to get the row the next move is in. (head + 1) 
        for i in self.ai_path:
            if nex_move in i: break
            move_in += 1
        
        #if the next move is one row down, then the only option is down
        if move_in > head_in: 
            head_inc()
            return "Down"
         #if the next move is one row up, then the only option is up
        if move_in < head_in : 
            head_inc()
            return "Up"
        
        # getting the collum / index that the head is in, in the row
        location_head = self.ai_path[head_in].index(self.head_place)
        # getting the collum / index that the next move is in, in the row
        location_move = self.ai_path[head_in].index(nex_move)
        
        # if the next move index is greater then, then move to the right
        if location_move > location_head : 
            head_inc()
            return "Right"
        
        # process of elimination, move to the left
        head_inc()
        return "Left"
    
    def key_input(self, event):
        '''
        injecting some of my own code into here. 
        This just checks to see if the spacebar was pressed, and if so to then
        let the snake AI play.
        '''
        if not self.crashed:
            key_pressed = event.keysym
            if key_pressed == 'space':
                # toggle ai_on, which voids/admits key imputs
                self.ai_on = not self.ai_on
                # Since the snake is ways starting 3 tiles long, the head will
                # be on tile 2, when starting the array at 0
                self.head_place = 2
                # Both skip_snake_len, and skip_turn work parallel with on another
                # creating a list to append the skipped tiles to
                self.skip_snake_len = []
                # creating a list to append how long the skipped tiles have be there
                self.skip_turn = []
                # let the games begin
                self.begin = True
            # Check if the pressed key is a valid key
            if self.check_if_key_valid(key_pressed) and not self.ai_on:
                # print(key_pressed)
                self.begin = True
                self.last_key = key_pressed
    

game_instance = SnakeAndApple()
game_instance.mainloop()
