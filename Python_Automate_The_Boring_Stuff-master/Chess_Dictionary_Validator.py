def proper_board():
    my_dic = {}
    my_piece_list = ['rook','knight','bishop','king','queen','bishop','knight','rook']
    #assuming that white takes 1 and 2, as black takes 7 and 8
    for tile in range(8):
        my_dic["1"+chr(97+tile)] = "w"+my_piece_list[tile]
        my_dic["2"+chr(97+tile)] = "wpawn"
        my_dic["7"+chr(97+tile)] = "bpawn"
        my_dic["8"+chr(97+tile)] = "b"+my_piece_list[7-tile]
    return my_dic
    
def improper_board(board = 0):
    my_dic = {}
    my_piece_list = ['rook','knight','bishop','king','queen','bishop','knight','rook']
    #Error of more peices
    if board == 1:
        for tile in range(8):
            my_dic["1"+chr(97+tile)] = "w"+my_piece_list[2]
            my_dic["2"+chr(97+tile)] = "wpawn"
            my_dic["7"+chr(97+tile)] = "bpawn"
            my_dic["8"+chr(97+tile)] = "b"+my_piece_list[4]
    #Error of nonexistant tiles
    elif board == 2:
        for tile in range(8):
            my_dic["1"+chr(99+tile)] = "w"+my_piece_list[2]
            my_dic["2"+chr(99+tile)] = "wpawn"
            my_dic["7"+chr(99+tile)] = "bpawn"
            my_dic["8"+chr(99+tile)] = "b"+my_piece_list[4]
            
    return my_dic

def board_checker(my_dic):
    my_tiles_list = []
    my_piece_dic = {}
    for tile, piece in my_dic.items():
        my_tiles_list.append(tile)
        my_piece_dic.setdefault(piece,0)
        my_piece_dic[piece] = my_piece_dic[piece]+1
    #checking if tiles work
    for tile in my_tiles_list:
        #checking that the number falls between 1-8
        if int(tile[0]) > 8 or int(tile[0]) < 1:
            return False
        #checking that the letter falls between lowercase a-h
        if ord(tile[1]) > 104 or ord(tile[1]) < 97:
            return False
    #counting all the pieces
    for piece, count in my_piece_dic.items():
        #checking for more than 8 pawns
        if 'pawn' in piece and count > 8:
            return False
        #checking for more than 1 king or queen
        elif ('king' in piece and count > 1) or ('queen' in piece and count > 1):
            return False
        #checking for more than 2 special pieces
        elif ('o' in piece or 't' in piece) and count > 2:
            return False
    return True
        

if __name__ == "__main__":
    print(board_checker(proper_board()))
    print(board_checker(improper_board(1)))
    print(board_checker(improper_board(2)))
    
