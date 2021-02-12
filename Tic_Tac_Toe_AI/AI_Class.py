# important imports
import Utils
import random

class AI:

    def __init__(self,board_snapshot,token,move_id,look_forward):
        # Incrementing the classes by 1 to keep log of how many are made
        Utils.classes += 1
        # Classes Personal copy of the board
        self.board_snapshot = board_snapshot
        # weither last move was 'x's or 'o's
        self.token = token
        # How many moves to look forward
        self.look_forward = look_forward 
        # What tile was chosen
        self.move_id = move_id
        # array holding all the child AI's
        self.CHILD_AIS = []
        # getting the weights of a move which also grabs the child's in process
        self.weight = round(self.get_weight(),6)
    
    # A function to select the branch with the most potential wins
    def best_move(self):
        print(f'''
The AI Is Looking {self.look_forward} Moves Ahead... 
{Utils.classes}'s Classes Were Created...
Moves & Weights...''')
        # sorting the childs from greatest to least
        self.CHILD_AIS.sort(key=lambda c: -1 * c.weight)
        # remove list
        rm = []
        # itterating through the childs in CHILD_AIS and adding to rm if not best pic
        for child in self.CHILD_AIS: 
            print(f'Tile : {child.move_id} | Weight : {child.weight*100}', end='')
            if child.weight != self.CHILD_AIS[0].weight: 
                rm.append(child)
                print(" <-- REMOVING MOVE")
            else: print()
        # removing the childs
        for child in rm: self.CHILD_AIS.remove(child)
        # if there are several moves with the same weight, pick a random one to add some variety
        if len(self.CHILD_AIS) > 1:
            move = self.CHILD_AIS[random.randrange(len(self.CHILD_AIS))].move_id
            mystr = 'Move Bank : '+' '.join(str(child.move_id) for child in self.CHILD_AIS)
            print('-'*len(mystr))
            print(mystr)
            print(f'Selecting Tile : {move}')
            return move
        # return the best move
        print(f'------------------\nSelecting Tile : {self.CHILD_AIS[0].move_id}')
        return self.CHILD_AIS[0].move_id
    
    # creating child AI's
    def create_child_state(self):
        # if we cant go forward anymore 
        # NOTE : if you want to controle the amount that you set forward instead
        # of always looking the furthest down the path, this is important
        if not self.look_forward : return 
        # filling out all of the child AI's in open spaces
        for index in range(9):
            if self.board_snapshot[index] == ' ':
                # create a copy of the list so we don't edit the parent list
                bsc = list(self.board_snapshot)
                # making the move
                bsc[index] = self.token
                # toggling the token
                other_token = Utils.AI if self.token == Utils.PLAYER else Utils.PLAYER
                # adding the child
                self.CHILD_AIS.append(AI(bsc,other_token,index,self.look_forward - 1))
            
    # A recursive function to get how many potential winning moves are present down the tree
    def get_weight(self):
        # if there is a winner, return 1 for AI return -1 for player
        for index in range(3):
            if (self.board_snapshot[index*3] == self.board_snapshot[index*3 + 1] and
                self.board_snapshot[index*3] == self.board_snapshot[index*3 + 2] and
                self.board_snapshot[index*3] != ' '):
                return 1  if self.board_snapshot[index*3] == Utils.AI else -1
            if (self.board_snapshot[index] == self.board_snapshot[index + 3] and
                self.board_snapshot[index] == self.board_snapshot[index + 6] and
                self.board_snapshot[index] != ' '):
                return 1 if self.board_snapshot[index] == Utils.AI else -1
        if (self.board_snapshot[0] == self.board_snapshot[4] and
            self.board_snapshot[0] == self.board_snapshot[8] and
            self.board_snapshot[0] != ' '):
            return 1  if self.board_snapshot[0] == Utils.AI else -1
        if (self.board_snapshot[2] == self.board_snapshot[4] and
            self.board_snapshot[2] == self.board_snapshot[6] and
            self.board_snapshot[2] != ' '):
            return 1 if self.board_snapshot[2] == Utils.AI else -1
        # if there is not a winner, see if there are child paths then call the function recursively
        self.create_child_state()
        if len(self.CHILD_AIS) > 0: 
            # diving by the length of childs, so no move exceeds -1, or 1. Returning the average path
            m =  sum([child.weight for child in self.CHILD_AIS])/len(self.CHILD_AIS)
            # Freeing up some memory
            if self.board_snapshot != Utils.board: del self.CHILD_AIS
            return m
        # if dead end
        return 0