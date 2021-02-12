# important imports
import Utils
import AI_Class

'''
GAME
----
'''
def game():
    # Resetting the varibles as well as getting who's turn it is
    Utils.reset_vals()
    ai_turn = bool(Utils.starting_input())
    # Keeping the screen clean
    print('\n'*Utils.CLEAR_COUNT)
    # Main game loop
    while True:
        if ai_turn:
            # We can only look foward at most, the amount of tiles that we have left
            # in the board, while the code will work if we give it a number
            # greater than the amount of tiles, due to printing out this varible
            # it would look silly if we only look 1 move ahead and the AI says 10
            tiles_left = sum([int(tile == ' ') for tile in Utils.board ])
            Utils.look_forward = tiles_left
            # Creating an AI objet 
            ai = AI_Class.AI(Utils.board,
                    Utils.AI,
                    -1,
                    Utils.look_forward)
            Utils.board[ai.best_move()] = Utils.AI
            # deleting the AI object to save memory since the AI and it's children
            # are taking up a lot of memory with the Mini-Max Algorithm
            del ai
            Utils.classes = -1
        else:
            # Humans turn
            Utils.get_user_input()
            print('\n'*Utils.CLEAR_COUNT)
        # toggling the turn
        ai_turn = not ai_turn
        # Seeing if the game is over
        winner = Utils.has_won()
        if winner == 1:
            print("Nice Try, But The AI Has Won!")
            Utils.show_board()
            Utils.AI_wins += 1
            return
        elif winner == -1:
            print("CONGRATS YOU BEAT THE AI!")
            Utils.show_board()
            Utils.player_wins += 1
            return
        if not ' ' in Utils.board:
            print("Close, But No Cigar... Tie!")
            Utils.show_board()
            Utils.game_ties += 1
            return
    
if __name__ == '__main__':
    print('''
+-------------------------------------------------------------------------------+
| The Mini-Max Algorithm is an algorithm that uses graph theory to determin     |
| the best next move. This alogrithm is a very powerful one, and is important   |
| to be in the tool kit of any machine learning programer. I have added a       |
| small twist to the Mini-Max algorithm, and that allows for the same AI code   |
| to be used for any state of the game (moving first or not). Instead of using  |
| a depth, I take the average of branches per node. This allows for the weights |
| to always be between -1 and 1.                                                |
+-------------------------------------------------------------------------------+''')
    game()
    while not bool(Utils.play_again()):
        print('\n'*Utils.CLEAR_COUNT)
        game()