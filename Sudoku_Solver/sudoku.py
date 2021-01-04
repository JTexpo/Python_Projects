import tkinter as tk
import numpy as np

# Creating a window for the GUI
window = tk.Tk()

# Creation a list to hold revious states of the boards
backup = []
# The structor that I chose to create for the board will be :
# Board[Box][Space][Guess_List]
# This makes a 9 x 9 x 9 = 729 varibles per board
# I chose to use dictionaries instead of lists,
# and I am aware that using a dictionary is not the best use for one here;
# however, it's my code and mentally it was easier for me to visualize it with dictionaries

# Creating the GUI for the user to have ease using the script
tiles = []
# This will group everyhing to be in boxes and not be in a verticle line.
# Slightly more logic in the beginning to benifit from it in the later.
# Running the script will show the initial assignment of all boxes
for i in range(9):
    for x in range(9):
        tiles.append(tk.Entry(window, width = 5))
        tiles[9*i+x].insert(0,"{} : {}".format(i+1,x+1))
        tiles[9*i+x].grid(row = ((int(i/3) * 3) + int(x/3)),
                          column = (x%3 + ((i%3) * 3))
                          )

# A method to clear all of the 
def clear_tiles():
    # Grabs the global varibles for modification
    global tiles
    global backup
    # Clearing the Backup
    backup = []
    # Clearing the tiles to have nothing written in them
    for tile in tiles:
        tile.delete(0,tk.END)
# Creating a Button to assign the method to
clear_btn = tk.Button(command = clear_tiles, text = "CLEAR!")
clear_btn.grid(row = 9, column = 1)

# First check of 4 to help the computer wittle down options
def box_check(dict_box,space_num):
    # If the tile has only 1 possiblity return to save time
    if len(dict_box[space_num]) == 1:
        return dict_box[space_num]

    # Making a copy of the list since I personally do not ever like editing directly
    my_list = list(dict_box[space_num])

    # For every item in the box
    for tile,guess in dict_box.items():
        # If the item has only 1 possibility
        # and that 1 possiblity is in the selected tiles guess list
        if (len(guess) == 1) and (guess[0] in my_list):
            # remove the guess from the guess list
            my_list.remove(guess[0])
            # Example :
            # 0 : [1,2,3]
            # 1 : [4]
            # 2 : [5,6]
            # 3 : [7]
            # 4 : [1,2,6,7,8,9] <-- here
            # 5 : [8,9]
            # 6 : [8,9]
            # 7 : [5,6]
            # 8 : [1,5]
            # 4 : [1,2,6,7,8,9] will match with 1 and 3 making the new list
            # 4 : [1,2,6,8,9] removing the 7
            # This is also why it's good to make a copy and not effect the instance.
            # Effecting the tile directly will cause for the loop to be more complicated than it is
            # and risk returning an empty list

    #returns list for assignment
    return my_list

def row_check(board,box_num,space_num):
    # If the tile has only 1 possiblity return to save time
    if len(board[box_num][space_num]) == 1:
        return board[box_num][space_num]

    # This is best explained with an example :
    # We are in box 7 (Bottom mid box) and tile 3 (mid left tile)
    box_row = int(box_num / 3) * 3
    # int(7/3) = 2
    # 2 * 3 = 6
    # box 6 is the bottom left box!
    guess_space = int(space_num / 3) * 3
    # int(3/3) = 1
    # 1 * 3 = 3
    # tile 3 is the middle left box!

    # Making a copy of the list since I personally do not ever like editing directly
    my_list = list(board[box_num][space_num])

    # 3 boxes in a board
    for i in range(3):
        # 3 tiles in a box
        for x in range(3):
            # This will move everything to the right slowly by one and then loop back over after ever 3
            guess = board[box_row+i][guess_space+x]
            # If the item has only 1 possibility
            # and that 1 possiblity is in the selected tiles guess list
            if (len(guess) == 1) and (guess[0] in my_list):
                # See box_check method for an example
                my_list.remove(guess[0])

    #returns list for assignment   
    return my_list

def collum_check(board,box_num,space_num):
    # If the tile has only 1 possiblity return to save time
    if len(board[box_num][space_num]) == 1:
        return board[box_num][space_num]

    # This is best explained with an example :
    # We are in box 5 (mid right box) and tile 1 (top mid tile)
    box_col = box_num % 3
    # 5 % 3 = 2
    # 2 is the top right box
    guess_space = space_num % 3
    # 1 % 3 = 1
    # one is the top middle tile
    # knowing that if we are to take the module of everything we will get : 0 1 2
    # the 0 1 2 tells us our placement of left center right

    # Making a copy of the list since I personally do not ever like editing directly
    my_list = list(board[box_num][space_num])

    # 3 boxes in a board
    for i in range(3):
        # 3 tiles in a box
        for x in range(3):
            # This is slightly more complicated than the row
            # Esentially adding 3 will move it down 1 collum
            # 0 3 6, are all the left boxes/tiles
            # 1 4 7, are all the middle boxes/tiles
            # 2 5 8, are all the right boxes/tiles
            guess = board[box_col+i*3][guess_space+x*3]
            # If the item has only 1 possibility
            # and that 1 possiblity is in the selected tiles guess list
            if (len(guess) == 1) and (guess[0] in my_list):
                # See box_check method for an example
                my_list.remove(guess[0])
            
    #returns list for assignment  
    return my_list


def adv_box_check(dict_box,space_num):
    # If the tile has only 1 possiblity return to save time
    if len(dict_box[space_num]) == 1:
        return dict_box[space_num]

    # Making a copy of the list since I personally do not ever like editing directly
    my_list = list(dict_box[space_num])

    # Looping throw all 9 spaces and seeing if our current space has a unique value.
    # Testing for uniqueness will limit the guessing that the computer will do.
    # This is important because we want our code to run fast!
    for i in range(9):
        # If we're looking at our space continue
        if i == space_num:
            continue
        # The one and only numpy operation that save me all the work of list minipulation
        # This will remove any values from the list that are found in a different list
        # While I could make code for it, I remembered using this before and why re-invent the wheel
        my_list = np.setdiff1d(my_list,dict_box[i]).tolist()

    # Checking to see if the list has only 1 unique value.
    # If it does we know that we want this value since no other tiles can have this value.
    # The check is for uniquness and if one tile is the only one that can have a 3
    # Then it must be the number 3 tile
    if len(my_list) == 1:
        return my_list

    # returning the initial list that was before we modified anything.
    # This is because if it doesn't have any uniqueness, then we learned nothing mor of the tile
    return dict_box[space_num]

# A method to see if everything is all figured out
def board_finished(board):
    # For ever box inn the board
    for i in range(9):
        # For every tile in the box
        for x in range(9):
            # If the tile does not have 1 guess in it, return.
            # Checking negatives is faster than positives since its more likely to occure in this case
            if len(board[i][x]) != 1:
                return False

    # Return true if everything only has one guess
    return True
        
# A method to solve the sudoku board
def solve():
    # Grabs the global varibles for modification
    global tiles
    global backup
    # Creating a board
    board = {}
    # Nine Boxes in a board
    for i in range(9):
        # Quick reminder, I am using dictionaries because visually when seeing the output it makes it easier for me to interpret
        # This will work fine with list too; however, its more kind for me to see
        # {0 : { 0 : [1,2,3,4,5,6,7,8,9] , 1 : [1,2,3,4,5,6,7,8,9], ... } , 1 : { ... } , ... }
        # I then knew quickly what I am looking at and don't have to wast time counting lists upon a quick print(board)
        board[i] = {}
        # Nine tiles in a box
        for x in range(9):
            # Grabbing the values inside of the tiles
            # This is where a good foundation helps. now we can group the tiles easily
            num = tiles[9*i+x].get()
            # Try to see if the value is a number, and if so to assign it to the board at the proper index
            try:
                if (int(num) > 0) and int(num) < 10:
                    board[i][x] = [int(num)]
                    continue
            except Exception as error:
                pass
            # If there was nothing in it, or a string, assign the box to being an open box and store all guesses
            board[i][x] = [1,2,3,4,5,6,7,8,9]
            
    # Yo dawg I heard you like methods so I got you some methods for your methods
    # This is because I will need to solve the board a few times over, and having this will save on code later.
    # I placed this method inside the method since it will reference local varibles insider here
    def simple_solve():
        # Itterate through the board 40 times
        # This number can be a lot shorter!
        # 40 times was what I believed to be a safe worse case scene, but with looking at how it solves it could really be 10 -> 20
        # 40 * 81 is 3240 times that this will be done, which I think is a tad excessive.
        # Reducing this too low may create too many backups, and I'd say storing more memory is far worse than waisting some time computing
        for i in range(40):
            # for boxes in board
            for box_num in range(9):
                # for spaces in boxes
                for space_num in range(9):
                    # Have the space do the box check
                    board[box_num][space_num] = box_check(board[box_num],space_num)
                    # We should NEVER get an empty list because then we have no guesses.
                    # If We get an empty list we throw a flag right away.
                    # 1 is a error flag
                    if len(board[box_num][space_num]) == 0:
                        tiles[box_num*9+space_num].delete(0,tk.END)
                        tiles[box_num*9+space_num].insert(0,"ERROR")
                        return 1
                    # Have the space do the row check
                    board[box_num][space_num] = row_check(board,box_num,space_num)
                    # We should NEVER get an empty list because then we have no guesses.
                    # If We get an empty list we throw a flag right away.
                    # 1 is a error flag
                    if len(board[box_num][space_num]) == 0:
                        tiles[box_num*9+space_num].delete(0,tk.END)
                        tiles[box_num*9+space_num].insert(0,"ERROR")
                        return 1
                    # Have the space do the collum check
                    board[box_num][space_num] = collum_check(board,box_num,space_num)
                    # We should NEVER get an empty list because then we have no guesses.
                    # If We get an empty list we throw a flag right away.
                    # 1 is a error flag
                    if len(board[box_num][space_num]) == 0:
                        tiles[box_num*9+space_num].delete(0,tk.END)
                        tiles[box_num*9+space_num].insert(0,"ERROR")
                        return 1
                    # Have the space do the secondary box (advance) check
                    board[box_num][space_num] = adv_box_check(board[box_num],space_num)
                    # We should NEVER get an empty list because then we have no guesses.
                    # If We get an empty list we throw a flag right away.
                    # 1 is a error flag
                    if len(board[box_num][space_num]) == 0:
                        tiles[box_num*9+space_num].delete(0,tk.END)
                        tiles[box_num*9+space_num].insert(0,"ERROR")
                        return 1

                    # If the board only has 1 guess, then print that pretty like for the user to see
                    if len(board[box_num][space_num]) == 1:
                        tiles[box_num*9+space_num].delete(0,tk.END)
                        tiles[box_num*9+space_num].insert(0,"{}".format(board[box_num][space_num][0]))
                    # If the board still has many guesses, just display the list and if the user ever wants they can manually fix it.
                    # NOTE THE USER SHOULD NEVER SEE THE LISTS UNLESS MESSING AROUND WITH THE BACKUP FEATURE
                    else:
                        tiles[box_num*9+space_num].delete(0,tk.END)
                        tiles[box_num*9+space_num].insert(0,"{}".format(board[box_num][space_num]))
                        
            # Check after checking all the tiles if the board is complete
            if board_finished(board):
                # 0 is a all good exit code
                return 0
            # If not loop again
        # 2 is an exit code which means more needs to be done. Mainly time to start guessing
        return 2

    # Before we start lets add the board to the backip to have as a reference incase stuff goes wrong
    backup.append(board)
    # Try to solve
    sodoku = simple_solve()
    # If in the first itteration it is solved or something went wrong, exit!
    # It is not the computers fault if something went wrong the first time, since the computer is just doing checks and not making guesses
    if (sodoku == 0) or (sodoku == 1):
        return

    # Advance solving time. This will require a lot of guesses and checks
    while True:
        # Since I have nested loops thi is my way of breaking them
        break_loops = False
        
        # The guess_risk is a way to pick which tile has the least amount of choices.
        # Ideally it would like to find something with 2, as then it can make a binary tree and that will be the quickest method
        # Sadly there will be some cases where there is 3 or more, and even 9 if giving it a blank board to solve.
        guess_risk = 9
        # For boxes in the board
        for box_num in range(9):
            # for tile in the boxes
            for space_num in range(9):
                # If the guess number is less than the risk, but a guess is still required to be made, make that be a guess
                # This will create a range between 2 <= guess <= 9
                if (len(board[box_num][space_num]) < guess_risk) and (len(board[box_num][space_num]) != 1):
                    guess_risk = len(board[box_num][space_num])
        # If somewhere down the line we made an empty list, revert to a previous save state.
        # THIS SHOULD NEVER EVER HAPPEN BUT IS A SECOND BACKUP
        if guess_risk == 0:
            board = backup.pop()
            continue

        # For boxes in the board
        for box_num in range(9):
            # for tile in the boxes
            for space_num in range(9):
                # If the tile is the first to match the guess risk
                if len(board[box_num][space_num]) == guess_risk:
                    # Hold the last element of the guesses for that tile
                    hold = board[box_num][space_num].pop()

                    # Add a dictionary to the backup and copy the entire board
                    # Sadly doing backup.append(board) will make a pointer to the board.
                    # Having a pointer to something that is changing is not good when trying to make a backup,
                    # so all of the board needed to be coppied manually
                    backup.append(dict())
                    # For boxes in the board
                    for i in range(9):
                        # for tile in the boxes
                        backup[len(backup)-1][i] = {}
                        for x in range(9):
                            # copy. NOTE using list(elm) prevents a pointer from being made
                            # Also, the board will have the alternate state of the guess as a backup.
                            # If the options were [2,7]. 7 would be removed as the current guess,
                            # and if something went wrong, that means that the right guess was 2!
                            backup[len(backup)-1][i][x] = list(board[i][x])

                    # Clearing the guesses for the board
                    board[box_num][space_num] = []
                    # Placing the one guess held in the start as true
                    board[box_num][space_num].append(hold)
                    # break loop
                    break_loops = True
                    break
            # break loop
            if break_loops == True:
                break

        # The computer attempts to solve
        sodoku = simple_solve()
        # If everything is solved quit
        if sodoku == 0:
            return
        # If an error was raised, go back to the previous saved state and try again
        if sodoku == 1:
            board = backup.pop()
        # if sodoku == 2, just continue doing what you're doing
# Creating a Button to assign the method to
solve_btn = tk.Button(command = solve, text = "SOLVE!")
solve_btn.grid(row = 9, column = 0)

# A method for going back 1 backup
def backup_save():
    # Grabs the global varibles for modification
    global backup
    # If there is no backup, quit
    if len(backup) == 0:
        return
    # If there is a backup assign the board to it
    board = backup.pop()
    # for box in board
    for box_num in range(9):
        # for tile in box
        for space_num in range(9):
            # assign the GUI fields equal to the values in the board. Same as in the solve loop
            if len(board[box_num][space_num]) == 1:
                tiles[box_num*9+space_num].delete(0,tk.END)
                tiles[box_num*9+space_num].insert(0,"{}".format(board[box_num][space_num][0]))
            else:
                tiles[box_num*9+space_num].delete(0,tk.END)
                tiles[box_num*9+space_num].insert(0,"{}".format(board[box_num][space_num]))
# Creating a Button to assign the method to
backup_save_btn = tk.Button(command = backup_save, text = "backup")
backup_save_btn.grid(row = 9, column = 4)
