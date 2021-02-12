'''
INITS
-----
'''
# Player and AI peices
PLAYER = 'o'
AI = 'x'
# Score Counter
player_wins = 0
AI_wins = 0
game_ties = 0
# Dictionary used for tokenizing user input
INPUT_DICT = {'a':0,'b':1,'c':2}
# varible to how many new lines to return
CLEAR_COUNT = 50
# these get reset with reset_vals, but so they can be referenced.
classes = -1
look_forward = 9
board = [' ']*9

'''
GAME FUNCTIONS
--------------
'''
# reseting game values
def reset_vals(): 
    global board, look_forward, classes
    look_forward = 9
    board = [' ']*9
    classes = 0
# visual for the board
def show_board():
    print(f'''  a   b   c
1 {board[0]} | {board[1]} | {board[2]}
  ---------
2 {board[3]} | {board[4]} | {board[5]}
  ---------
3 {board[6]} | {board[7]} | {board[8]}''')
# A function to determin the winner 1 is the AI -1 is the player
def has_won():
    for index in range(3):
        # row check
        if ( board[index*3] == board[index*3 + 1] and
             board[index*3] == board[index*3 + 2] and
             board[index*3] != ' '):
            return 1 if board[index*3] == AI else -1
        # col check
        if ( board[index] == board[index + 3] and
             board[index] == board[index + 6] and
             board[index] != ' '):
            return 1 if board[index] == AI else -1
    # diangle check 1
    if ( board[0] == board[4] and
         board[0] == board[8] and
         board[0] != ' '):
        return 1 if board[0] == AI else -1
    # diangle check 2
    if ( board[2] == board[4] and
         board[2] == board[6] and
         board[2] != ' '):
        return 1 if board[2] == AI else -1
    # no winner
    return 0
'''
INPUT FUNCTIONS
---------------
'''
# a function to see if the user wants to play again
def play_again():
    print('''
+--------------------+
| Would You Like To: |
|  1. Play Again     |
|  2. Quit           |
+--------------------+''')
    while True:
        usrIn = input(': ')
        try:
            usrIn = int(usrIn)
            if usrIn == 1 or usrIn == 2: return usrIn - 1
            print("[*] Please Enter Either '1' or '2'")
        except:
            print("[*] Please Enter Either '1' or '2'")
# A function to get the user move
def get_user_input():
    print(f'''
+----------------------------------------------------+
| You Are '{PLAYER}'s                                       |
| Wins : {player_wins} Losses : {AI_wins} Ties : {game_ties}                       |
| Please Enter The Letter First Than Number : ex. a1 |
+----------------------------------------------------+''')
    show_board()
    while True:
        usrIn = input(': ')
        try:
            usrIn = usrIn.lower()
            if (usrIn[0] in INPUT_DICT and 
                int(usrIn[1]) < 4 and 
                int(usrIn[1]) > 0 ):
                spot = INPUT_DICT[usrIn[0]] + (int(usrIn[1]) - 1) * 3
                if board[spot] == ' ':
                    board[spot] = PLAYER
                    return
            else:
                print('[*] Please Enter The Letter First Than Number : ex. a1')
        except:
            print('[*] Please Enter The Letter First Than Number : ex. a1')
# A function to start the code
def starting_input():
    print('''
+-----------------------------------------------------+
| Tic Tac Toe Mini-Max AI With A Twist. Would You :   |
|  1. Like To Go First (* CHANCE TO WIN *)            |
|  2. Like The AI To Go First (* IMPOSSIBLE TO WIN *) |
+-----------------------------------------------------+''')
    while True:
        usrIn = input(': ')
        try:
            usrIn = int(usrIn)
            if usrIn == 1 or usrIn == 2: return usrIn - 1
            print("[*] Please Enter Either '1' or '2'")
        except:
            print("[*] Please Enter Either '1' or '2'")