from typing import List, Tuple
from copy import deepcopy

from game import HIT_UNSANK_SHIP_CODE, HIT_EMPTY_CODE, UNHIT_CODE


def is_valid_ship_move(
    board: List[List[int]],
    x_position: int,
    y_position: int,
    ship_length: int,
    is_vertical: bool,
) -> bool:
    """A function to detect if a ship could exist at the location on a grid.

    Args:
        board (List[List[int]]): The battleship map. ex
            [
                [ 0 0 0 ],
                [ 0 0 0 ],
                [ 0 0 0 ]
            ]
        x_position (int): The x position that the top left of the ship will be
        y_position (int): The y position that the top left of the ship will be
        ship_length (int): How long the ship is
        is_vertical (bool): If the ship is along the x or y axis

    Returns:
        bool: An indicator of if the move is valid or not
    """
    # board should be a square, and we are getting how long it is incase we exceed the length
    board_size = len(board)

    # Vertical check
    if is_vertical:
        # itterating over the range of vertical tiles
        for row in range(y_position, y_position + ship_length):
            # if the row is outside of the board bounds, or is a hit tile
            if row >= board_size or board[row][x_position] < UNHIT_CODE:
                return False
        return True
    
    # Horizontal check
    # itterating over the column of vertical tiles
    for column in range(x_position, x_position + ship_length):
        # if the column is outside of the board bounds, or is a hit tile
        if column >= board_size or board[y_position][column] < UNHIT_CODE:
            return False
    return True


def find_all_possible_ship_moves(
    board: List[List[int]], ship_length: int
) -> List[List[int]]:
    """_summary_

    Args:
        board (List[List[int]]): The battleship map. ex
            [
                [ 0 0 0 ],
                [ 0 0 0 ],
                [ 0 0 0 ]
            ]
        ship_length (int): How long the ship is

    Returns:
        List[List[int]]: Modified battleship map. ex
            [
                [ 2 3 2 ],
                [ 3 4 3 ],
                [ 2 3 2 ]
            ]
            notice that the map is more dense the closer we get to the middle, that is because there are more possibilities
    """
    # Deep copy, because python will make nested copys be references
    board = deepcopy(board)

    # itterating over the rows on the board
    for row_index, row in enumerate(board):
        # itterating over the columns of the board
        for column_index, column in enumerate(row):

            # Checking if the ship can be vertically placed, and if so adding +1 to the impacted tiles
            if is_valid_ship_move(
                board=board,
                x_position=column_index,
                y_position=row_index,
                ship_length=ship_length,
                is_vertical=True,
            ):
                for eligible_row in range(row_index, row_index + ship_length):
                    board[eligible_row][column_index] += 1

            # Checking if the ship can be horizontally placed, and if so adding +1 to the impacted tiles
            if is_valid_ship_move(
                board=board,
                x_position=column_index,
                y_position=row_index,
                ship_length=ship_length,
                is_vertical=False,
            ):
                for eligible_column in range(column_index, column_index + ship_length):
                    board[row_index][eligible_column] += 1

    return board


def find_best_move_hunt(
    board: List[List[int]], ship_lengths: List[int]
) -> Tuple[List[List[int]], int, int]:
    """A function to find the best move using the standard population distribution

    Args:
        board (List[List[int]]): The battleship map. ex
            [
                [ 0 0 0 ],
                [ 0 0 0 ],
                [ 0 0 0 ]
            ]
        ship_length (int): How long the ship is

    Returns:
        Tuple[List[List[int]], int, int]: 
            board (List[List[int]]): Modified battleship map. ex
            [
                [ 2 3 2 ],
                [ 3 4 3 ],
                [ 2 3 2 ]
            ]
            best_x int: The best X value of the highest int in the board (example above would return 1)
            best_y int: The best Y value of the highest int in the board (example above would return 1)
    """
    # Deep copy, because python will make nested copys be references
    board = deepcopy(board)
    # Initializing our values to be low, so everything can surpass it
    best_x = -1
    best_y = -1
    best_move_score = -1

    # For all the ships on the board, map out the standard population density
    for ship_length in ship_lengths:
        board = find_all_possible_ship_moves(board=board, ship_length=ship_length)

    # Find the max value, and if found update, best_x, best_y, and best_move_score
    for row_index, row in enumerate(board):
        if max(row) <= best_move_score:
            continue

        best_move_score = max(row)
        best_x = row.index(best_move_score)
        best_y = row_index

    return board, best_x, best_y


def find_splash_radius(
    board: List[List[int]], x_position: int, y_position: int
) -> List[List[int]]:
    """A function to find the NSEW splash values for a hit location

    Args:
        board (List[List[int]]): The battleship map. ex
            [
                [ 0 0  0 ],
                [ 0 0  0 ],
                [ 0 0 -2 ]
            ]
        x_position (int): The x position that the top left of the ship will be
        y_position (int): The y position that the top left of the ship will be

    Returns:
        List[List[int]]: Modified battleship map. ex
            [
                [ 0 0  1 ],
                [ 0 0  2 ],
                [ 1 2 -2 ]
            ]
    """
    # Deep copy, because python will make nested copys be references
    board = deepcopy(board)
    # board should be a square, and we are getting how long it is incase we exceed the length
    board_size = len(board)

    # up
    itteration = -1
    for row_index in range(y_position, -1, -1):
        itteration += 1
        # ending the loop because we can not have a ship that passes through a hit empty location
        if board[row_index][x_position] == HIT_EMPTY_CODE:
            break
        if board[row_index][x_position] == HIT_UNSANK_SHIP_CODE:
            continue
        board[row_index][x_position] += board_size - itteration
    # down
    itteration = -1
    for row_index in range(y_position, board_size, 1):
        itteration += 1
        # ending the loop because we can not have a ship that passes through a hit empty location
        if board[row_index][x_position] == HIT_EMPTY_CODE:
            break
        if board[row_index][x_position] == HIT_UNSANK_SHIP_CODE:
            continue
        board[row_index][x_position] += board_size - itteration
    # left
    itteration = -1
    for column_index in range(x_position, -1, -1):
        itteration += 1
        # ending the loop because we can not have a ship that passes through a hit empty location
        if board[y_position][column_index] == HIT_EMPTY_CODE:
            break
        if board[y_position][column_index] == HIT_UNSANK_SHIP_CODE:
            continue
        board[y_position][column_index] += board_size - itteration
    # right
    itteration = -1
    for column_index in range(x_position, board_size, 1):
        itteration += 1
        # ending the loop because we can not have a ship that passes through a hit empty location
        if board[y_position][column_index] == HIT_EMPTY_CODE:
            break
        if board[y_position][column_index] == HIT_UNSANK_SHIP_CODE:
            continue
        board[y_position][column_index] += board_size - itteration

    return board


def find_best_move_target(board: List[List[int]]) -> Tuple[List[List[int]], int, int]:
    """A function to get the best splash moves, knowing that we hit a ship

    Args:
        board (List[List[int]]): The battleship map. ex
            [
                [ 0 0  0 ],
                [ 0 0  0 ],
                [ 0 0 -2 ]
            ]

    Returns:
        Tuple[List[List[int]], int, int]: 
            board (List[List[int]]): Modified battleship map. ex
            [
                [ 0 0  1 ],
                [ 0 0  2 ],
                [ 1 2 -2 ]
            ]
            best_x int: The best X value of the highest int in the board (example above would return 1)
            best_y int: The best Y value of the highest int in the board (example above would return 1)
    """
    # Deep copy, because python will make nested copys be references
    board = deepcopy(board)
    best_x = -1
    best_y = -1
    # Initializing our values to be low, so everything can surpass it
    best_move_score = -1

    # itterating over the rows
    for row_index, row in enumerate(board):
        # doing a quick check to see if this is the row that contains a hit ship, and if not to skip
        if not (HIT_UNSANK_SHIP_CODE in row):
            continue

        # we dont know if its just 1 index or many
        for column_index, column in enumerate(row):
            # checking if the column value is our hit ship value
            if column != HIT_UNSANK_SHIP_CODE:
                continue

            # updating the board with the splash radius
            board = find_splash_radius(
                board=board, x_position=column_index, y_position=row_index
            )

    # Find the max value, and if found update, best_x, best_y, and best_move_score
    for row_index, row in enumerate(board):
        if max(row) <= best_move_score:
            continue

        best_move_score = max(row)
        best_x = row.index(best_move_score)
        best_y = row_index

    return board, best_x, best_y


def find_best_move(
    board: List[List[int]], ship_lengths: int
) -> Tuple[List[List[int]], int, int]:
    """A function to find the best move for the AI to make

    Args:
        board (List[List[int]]): The battleship map. ex
            [
                [ 0 0 0 ],
                [ 0 0 0 ],
                [ 0 0 0 ]
            ]
        ship_length (int): How long the ship is

    Returns:
        Tuple[List[List[int]], int, int]: 
            board (List[List[int]]): Modified battleship map. ex
            [
                [ 2 3 2 ],
                [ 3 4 3 ],
                [ 2 3 2 ]
            ]
            best_x int: The best X value of the highest int in the board (example above would return 1)
            best_y int: The best Y value of the highest int in the board (example above would return 1)
    """
    for row_index, row in enumerate(board):
        if not (HIT_UNSANK_SHIP_CODE in row):
            continue
        return find_best_move_target(board=board)
    return find_best_move_hunt(board=board, ship_lengths=ship_lengths)
