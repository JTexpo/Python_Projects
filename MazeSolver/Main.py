import tkinter as tk

size_of_board = 600
rows = 30
cols = rows

# The mode : [the colour, the id]
mode_to_board = {
    "draw":['black','wall'],
    "erase":['white','empty'],
    "start":['red','start'],
    "end":['green','end']
    }

# // -- A class used to define each point on the graph that is a child -- //
class node:
    # // -- Init Function -- //
    def __init__(self,x,y,parent):
        # The cells/nodes X and Y value as well as the parent which should be type class node
        self.x = x
        self.y = y
        self.parent = parent

# // -- The Application -- //
class MazeSolver:
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
        self.window.title("Maze Solver V1.0")

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
        # Creating the start mode button
        self.start_mode_btn = tk.Button(self.top_frame,text='start',command=self.start_mode,bg="gray")
        self.start_mode_btn.pack(side=tk.LEFT)
        # Creating the end mode button
        self.end_mode_btn = tk.Button(self.top_frame,text='end',command=self.end_mode,bg="gray")
        self.end_mode_btn.pack(side=tk.LEFT)

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
        # Creating the solve button
        self.solve_btn = tk.Button(self.bottom_frame,text='solve',command=self.solve,bg="gray")
        self.solve_btn.pack(side=tk.LEFT)

        # Initalizing the board on init of the class
        self.initialize_board()

    def edit_tiles(self,event):
        # If we are within the regins of the canvas
        # I use a not to the logic because I dont want to work with overly indented code
        if not (
            (event.x >= 0) and 
            (event.x <= size_of_board) and 
            (event.y >= 0) and 
            (event.y <= size_of_board)
            ): return
        # Using the dictionary at the top to be able to made the drawl compact
        self.canvas.create_rectangle(
            int(event.x/self.row_spacing)*self.row_spacing,
            int(event.y/self.column_spacing)*self.column_spacing,
            int(event.x/self.row_spacing)*self.row_spacing+self.row_spacing,  
            int(event.y/self.column_spacing)*self.column_spacing+self.column_spacing,
            fill = mode_to_board[self.mode][0])
        # An If statement to remove any duplicates of start and end as there can only be one
        if ((self.mode in ['start','end']) and (any(self.mode in row for row in self.board))):
            # a boolean to help potentially lower the big O 
            break_loop = False
            # A counter for the row that we are on
            loc_y_cord = -1
            # For loop to find the duplicate start or end point
            for row in self.board:
                # Since we started at -1, +1 to it will make us start at 0
                loc_y_cord += 1
                for col in row:
                    # If we find the tile with the duplicate
                    if (col == self.mode):
                        # Set the x and y values of the duplicate
                        loc_x_cord = row.index(col)
                        break_loop = True
                        break
                # hopefully lowering big O
                if break_loop: break
            # If the duplicate is not in the same tile as what our mouse is over
            # This is so we do not delete if we are moving over the same tile
            if not ((loc_y_cord == int(event.y/self.column_spacing)) and 
            (loc_x_cord == int(event.x/self.column_spacing))):
                # Set the tile to white to let the user know and change the board state
                self.canvas.create_rectangle(
                    loc_x_cord*self.row_spacing,
                    loc_y_cord*self.column_spacing,
                    loc_x_cord*self.row_spacing+self.row_spacing,
                    loc_y_cord*self.column_spacing+self.column_spacing,
                    fill = 'white')
                self.board[loc_y_cord][loc_x_cord] = 'empty'
        # update the board
        self.board[int(event.y/self.column_spacing)][int(event.x/self.row_spacing)] = mode_to_board[self.mode][1]

    # A function to retyrn all the child nodes that a node has
    def get_child(self,parent_node):
        # Creating a list to be fild with child nodes, these should all be of the type class node
        childes = []
        # 4 if statements, I know it looks gross, but I cant think of better logic at the moment
        # Each if statement is nested as such because if we call a value outside of the range of the board
        # we could cause the code to crash with an error

        # Checking the bottom tile
        if (parent_node.y != rows-1):
            if (self.board[parent_node.y+1][parent_node.x] in ['empty','end']):
                self.board[parent_node.y+1][parent_node.x] = 'child'
                childes.append(node(parent_node.x,parent_node.y+1,parent_node))
        # Checking the right tile
        if (parent_node.x != cols-1):
            if (self.board[parent_node.y][parent_node.x+1] in ['empty','end']):
                self.board[parent_node.y][parent_node.x+1] = 'child'
                childes.append(node(parent_node.x+1,parent_node.y,parent_node))
        # Checking the top tile
        if (parent_node.y != 0):
            if (self.board[parent_node.y-1][parent_node.x] in ['empty','end']):
                self.board[parent_node.y-1][parent_node.x] = 'child'
                childes.append(node(parent_node.x,parent_node.y-1,parent_node))
        # Checking the left tile
        if (parent_node.x != 0):
            if (self.board[parent_node.y][parent_node.x-1] in ['empty','end']):
                self.board[parent_node.y][parent_node.x-1] = 'child'
                childes.append(node(parent_node.x-1,parent_node.y,parent_node))
        # Returning all of the childs that were found
        return childes

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
                self.board[y].append('empty')
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

    def solve(self):
        row_counter = -1
        startx = -1
        endx = -1
        for row in self.board:
            row_counter += 1
            for col in row:
                if col == 'start':
                    startx = row.index(col)
                    starty = int(row_counter)
                if col == 'end':
                    endx = row.index(col)
                    endy = int(row_counter)
                if col == 'child':
                    self.canvas.create_rectangle(
                        row.index(col)*self.row_spacing,
                        row_counter*self.column_spacing,
                        row.index(col)*self.row_spacing+self.row_spacing,
                        row_counter*self.column_spacing+self.column_spacing,
                        fill = 'white')
                    self.board[row_counter][row.index(col)] = 'empty'

        if ((startx == -1)or(endx == -1)):
            return

        startNode = node(startx,starty,None)

        activeList = []
        queueList = []
        childs = self.get_child(startNode)
        activeList = list(childs)

        while ((activeList != []) or (queueList != [])):
            for active_node in activeList:
                childs = self.get_child(active_node)
                queueList = queueList + childs
            for child_node in queueList:
                if ((child_node.x == endx) and (child_node.y == endy)):
                    self.board[child_node.y][child_node.x] = 'end'
                    while(child_node.parent.parent != None):
                        child_node = child_node.parent
                        self.canvas.create_rectangle(
                            child_node.x*self.row_spacing,
                            child_node.y*self.column_spacing,
                            child_node.x*self.row_spacing+self.row_spacing,
                            child_node.y*self.column_spacing+self.column_spacing,
                            fill = 'blue')
                    return
            activeList = list(queueList)
            queueList = []
            

    def draw_mode(self):
        self.mode = "draw"
        self.mode_label.config(text=f"Mode : {self.mode}")
    def erase_mode(self):
        self.mode = "erase"
        self.mode_label.config(text=f"Mode : {self.mode}")
    def start_mode(self):
        self.mode = "start"
        self.mode_label.config(text=f"Mode : {self.mode}")
    def end_mode(self):
        self.mode = "end"
        self.mode_label.config(text=f"Mode : {self.mode}")

solver = MazeSolver()
solver.mainloop()