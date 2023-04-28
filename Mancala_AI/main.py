"""
https://endlessgames.com/wp-content/uploads/Mancala_Instructions.pdf

For 2 players – Ages 7 to Adult
Mancala is an ancient family of board games, and there are numerous variants. This is a version of the basic game, known as two-rank Mancala and also known as Kalah.

Contents:
1 Mancala board
48 colored plastic pieces (also called “stones”)

Set Up:
The Mancala board is made up of two rows of six pockets (also called “holes,” or “pits”) each. Four pieces are placed in each of the 12 pockets. The color of the pieces is irrelevant.
Each player has a “store” (also called a “Mancala”) to his/her right side of the Mancala board.

Object:
The object of the game is to collect the most pieces by the end of the game.

Game Play:
1. The game begins with one player picking up all of the pieces in any one of the pockets on his/her side.
2. Moving counter-clockwise, the player deposits one of the stones in each pocket until the stones run out.
3. If you run into your own Mancala (store), deposit one piece in it. If you run into your opponent's Mancala, skip it and
continue moving to the next pocket.
4. If the last piece you drop is in your own Mancala, you take another turn.
5. If the last piece you drop is in an empty pocket on your side, you capture that piece and any pieces in the pocket directly
opposite.
6. Always place all captured pieces in your Mancala (store).
7. The game ends when all six pockets on one side of the Mancala board are empty.
8. The player who still has pieces on his/her side of the board when the game ends captures all of those pieces. 
9. Count all the pieces in each Mancala. The winner is the player with the most pieces.
© 2015 Endless Games, Inc. All Rights Reserved.
"""
from typing import Tuple
import copy


def print_board(board: dict, player_1: str = "P 1", player_2: str = "P 2") -> None:
    """A function to display the board

    Args:
        board (dict): Schema
        {
            "top"          : [4, 4, 4, 4, 4, 4],
            "bottom"       : [4, 4, 4, 4, 4, 4],
            "top_score"    : 0,
            "bottom_score" : 0
        }
    """
    print(
        f"""
      6  5  4  3  2  1
+---+--+--+--+--+--+--+---+
|{player_1}|{'|'.join(f'{item:2}' for item in reversed(board['top']))}|   | <- PLAYER 1
|{board["top_score"]:3}+--+--+--+--+--+--+{board["bottom_score"]:3}|
|   |{board["bottom"][0]:2}|{board["bottom"][1]:2}|{board["bottom"][2]:2}|{board["bottom"][3]:2}|{board["bottom"][4]:2}|{board["bottom"][5]:2}|{player_2}| PLAYER 2 ->
+---+--+--+--+--+--+--+---+
      1  2  3  4  5  6
"""
    )
    return


def move_piece(board: dict, tile: int, turn: str) -> Tuple[dict, bool]:
    """A function to preform the moves of the user

    Args:
        board (dict): Schema
        {
            "top"          : [4, 4, 4, 4, 4, 4],
            "bottom"       : [4, 4, 4, 4, 4, 4],
            "top_score"    : 0,
            "bottom_score" : 0
        }
        tile (int): the index of the list
        turn (str): 'top' or 'bottom'

    Returns:
        Tuple[dict, bool]:
            board (dict): Schema
            {
                "top"          : [4, 4, 4, 4, 4, 4],
                "bottom"       : [4, 4, 4, 4, 4, 4],
                "top_score"    : 0,
                "bottom_score" : 0
            }
            go_again (bool): indicats if the user is able ot make another turn
    """
    pieces = board[turn][tile]
    board[turn][tile] = 0
    location = turn
    go_again = False

    # 2. Moving counter-clockwise, the player deposits one of the stones in each pocket until the stones run out.
    while pieces > 0:
        go_again = False
        pieces -= 1
        tile += 1

        if tile < len(board[location]):
            board[location][tile] += 1
            continue

        # 3. If you run into your own Mancala (store), deposit one piece in it.
        # If you run into your opponent's Mancala, skip it and continue moving to the next pocket.
        # 4. If the last piece you drop is in your own Mancala, you take another turn.
        if location == turn:
            board[f"{turn}_score"] += 1
            go_again = True
        else:
            pieces += 1

        location = "bottom" if location == "top" else "top"
        tile = -1

    # OPTIONAL RULE :
    # Some people like to play where if you land on a populated space on your side, you get to go again using that tile
    # If that is the rules that you like, please uncomment the codeblock below
    """
    if (location == turn) and (board[location][tile] > 1):
        return move_piece(board, tile, turn)
    """

    # 5. If the last piece you drop is in an empty pocket on your side,
    # you capture that piece and any pieces in the pocket directly opposite.
    # UNLESS, theres nothing directly in the pocket next to it
    # 6. Always place all captured pieces in your Mancala (store).
    inverse_location = "bottom" if location == "top" else "top"
    if (
        (location == turn)
        and (board[location][tile] == 1)
        and (board[inverse_location][len(board[inverse_location]) - 1 - tile] != 0)
    ):
        board[f"{turn}_score"] += (
            1 + board[inverse_location][len(board[inverse_location]) - 1 - tile]
        )
        board[location][tile] = 0
        board[inverse_location][len(board[inverse_location]) - 1 - tile] = 0

    # 7. The game ends when all six pockets on one side of the Mancala board are empty.
    # 8. The player who still has pieces on his/her side of the board when the game ends captures all of those pieces.
    if (not any(board["top"])) or (not any(board["bottom"])):
        board["top_score"] += sum(board["top"])
        board["bottom_score"] += sum(board["bottom"])

        board["top"] = [0] * len(board["top"])
        board["bottom"] = [0] * len(board["bottom"])

        go_again = False

    return board, go_again


def is_viable_move(board: dict, tile: int, turn: str) -> bool:
    """A validation function to determin if a move is viable

    Args:
        board (dict): Schema
        {
            "top"          : [4, 4, 4, 4, 4, 4],
            "bottom"       : [4, 4, 4, 4, 4, 4],
            "top_score"    : 0,
            "bottom_score" : 0
        }
        tile (int): the index of the list
        turn (str): 'top' or 'bottom'

    Returns:
        bool: if the space is a valid space to choose
    """
    if tile >= len(board[turn]) or tile < 0:
        return False
    return bool(board[turn][tile])


def minimax_mancala(
    board: dict, ai_side: str, turn: str, depth: int
) -> Tuple[int, int]:
    """A function to calculate the minimax algorithm for a given board

    Args:
        board (dict): Schema
        {
            "top"          : [4, 4, 4, 4, 4, 4],
            "bottom"       : [4, 4, 4, 4, 4, 4],
            "top_score"    : 0,
            "bottom_score" : 0
        }
        ai_side (str): 'top' or 'bottom'
        turn (str): 'top' or 'bottom'
        depth (int): How deep that you want the AI to look ahead, *WARNING* larger depths require more CPU power

    Returns:
        Tuple[int, int]:
            score (int): the likely hood of the move being the best move
                - this is used in recursion for finding the best move
            move (int) : the recommended minimax move
                - this is used in decision making for executing the best move
    """
    AI = ai_side
    PLAYER = "bottom" if AI == "top" else "top"
    best_move = -1

    # If the game is over, or the max depth is reached.
    # The delta of the AI - PLAYER is what I believe to give the best result, as it will cause the algorithm to strive for large number victories
    if (not any(board["top"])) or (not any(board["bottom"])) or depth <= 0:
        return board[f"{AI}_score"] - board[f"{PLAYER}_score"], best_move

    # Finding the move which will give the most points to the AI
    if AI == turn:
        # only uphill from here
        best_score = float("-inf")

        possible_moves = [
            move for move in range(len(board[AI])) if is_viable_move(board, move, AI)
        ]

        for move in possible_moves:
            # preforming a deepcopy so we don't accidently overwrite moves by referencing the same list
            board_copy = copy.deepcopy(board)
            board_copy, go_again = move_piece(board_copy, move, turn)

            # mancala is one of those games where you can get two moves.
            # In testing, I found that not decressing the depth for the multimove results in the best AI
            if go_again:
                points, _ = minimax_mancala(board_copy, AI, AI, depth)
            else:
                points, _ = minimax_mancala(board_copy, AI, PLAYER, depth - 1)

            # The MAX part of minimax. Finding the MAX output for the AI
            if points > best_score:
                best_move = move
                best_score = points

    # Finding the move which will give the least points to the PLAYER
    elif PLAYER == turn:
        best_score = float("inf")
        possible_moves = [
            move
            for move in range(len(board[PLAYER]))
            if is_viable_move(board, move, PLAYER)
        ]

        for move in possible_moves:
            # preforming a deepcopy so we don't accidently overwrite moves by referencing the same list
            board_copy = copy.deepcopy(board)
            board_copy, go_again = move_piece(board_copy, move, turn)

            # mancala is one of those games where you can get two moves.
            # In testing, I found that not decressing the depth for the multimove results in the best AI
            if go_again:
                points, _ = minimax_mancala(board_copy, AI, PLAYER, depth)
            else:
                points, _ = minimax_mancala(board_copy, AI, AI, depth - 1)

            # The MIN part of minimax. Finding the MIN output for the PLAYER
            if points < best_score:
                best_move = move
                best_score = points

    return best_score, best_move


def get_player_type() -> str:
    """A function to get the players type (top goes first)

    Returns:
        str: 'top' or 'bottom'
    """
    while True:
        player_input = input(
            "Please Enter Which Player You Want To Be :\n1. Player 1\n2. Player 2\n:"
        )
        if "quit" in player_input.lower():
            quit()
        elif "1" in player_input:
            return "top"
        elif "2" in player_input:
            return "bottom"
        print("Please Make Sure You Are Entering One Of The Two Options Listed.")


def get_player_move(board: dict, turn: str) -> int:
    """A function to get the players move

    Args:
        board (dict): Schema
        {
            "top"          : [4, 4, 4, 4, 4, 4],
            "bottom"       : [4, 4, 4, 4, 4, 4],
            "top_score"    : 0,
            "bottom_score" : 0
        }
        turn (str): 'top' or 'bottom'

    Returns:
        int: a valid move of the player
    """
    while True:
        player_move = input("Please Select A Move.\n:")
        if "quit" in player_move.lower():
            quit()
        try:
            player_move = int(player_move) - 1
        except ValueError:
            print("Please Make Sure To Enter A Valid Number.")
            continue

        if is_viable_move(board, player_move, turn):
            return player_move

        print("Sorry, That Is Not A Valid Move.")


if __name__ == "__main__":
    # Default board, feel free to update if you know what you're doing and want a more interesting game.
    # The code should be set up mostly generic enough to handle different boards / piece amount
    board = {
        "top": [4, 4, 4, 4, 4, 4],
        "bottom": [4, 4, 4, 4, 4, 4],
        "top_score": 0,
        "bottom_score": 0,
    }

    # Mapping for how confident the algorithm is on winning the game (ballpark)
    total_pieces = sum(board["top"]) + sum(board["bottom"])
    winning_confidence_mapping = {
        -(total_pieces // 8): "Terrible",
        -(total_pieces // total_pieces): "Bad",
        total_pieces // 16: "Possible",
        total_pieces // 8: "Good",
        total_pieces + 1: "Certain",
    }

    # Displaying the board so the user know what they are selecting
    print_board(board)
    # Collecting what type the user is
    PLAYER = get_player_type()

    # Some final inits before starting the game
    PRINT_P1 = "YOU" if PLAYER == "top" else "CPU"
    PRINT_P2 = "CPU" if PLAYER == "top" else "YOU"
    AI = "bottom" if PLAYER == "top" else "top"
    MAX_DEPTH = 6

    # Top always goes first, feel free to change if you want to be a reble
    turn = "top"

    # While the games not over!!!
    while not ((not any(board["top"])) or (not any(board["bottom"]))):

        # Players move
        if turn == PLAYER:
            # Getting the players move
            move = get_player_move(board, PLAYER)

            # Updating the board
            board, go_again = move_piece(board, move, PLAYER)

        # AI's move
        elif turn == AI:
            # Getting the AI's move with the Minimax function
            best_score, move = minimax_mancala(board, AI, turn, MAX_DEPTH)

            # Visual aid to show of confident the minimax algorithm is in winning
            winning_confidence = ""
            for score, confidence in winning_confidence_mapping.items():
                if score < best_score:
                    continue
                winning_confidence = confidence
                break
            print(f"AI Moved : {move+1}\nChance of Winning : {winning_confidence}")

            # Updating the board
            board, go_again = move_piece(board, move, AI)

        # 4. If the last piece you drop is in your own Mancala, you take another turn.
        if not go_again:
            turn = "bottom" if turn == "top" else "top"

        # Shows the new baord
        print_board(board, PRINT_P1, PRINT_P2)

    # WIN / LOSS / DRAW
    if board[f"{PLAYER}_score"] > board[f"{AI}_score"]:
        print(
            f"Congrats! You won when the AI looks {MAX_DEPTH} moves ahead. For more of a challenge try increasing the MAX_DEPTH value."
        )
    elif board[f"{PLAYER}_score"] < board[f"{AI}_score"]:
        print(
            f"Nice try, but the machines win this time! For an easier game try decreasing the MAX_DEPTH value."
        )
    else:
        print(f"DRAW! Are you too looking {MAX_DEPTH} moves ahead?")
