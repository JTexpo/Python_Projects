from typing import List
import random

PLAYER_TOKEN = "O"
FLOOR_CHAR = "▒"
AIR_CHAR = " "

EVOLUTION_CHANCE = 0.2
GEO_MODIFY_BACK = 50

STARTING_X = 3
STARTING_Y = 0


class GeoPerson:
    def __init__(self, moves: List[int], x_position: int, y_position: int, name: str):
        """The Geo People!

        Args:
            moves (List[int]): A list of 1's and 0's.
                1 = Jump
                0 = Don't Jump
            x_position (int): The X position that the Geo Person will be on the board
            y_position (int): The starting Y position the Geo Person will be
                *NOTE* 0, is ideal, because then this is a moving object for someone to easily find and understand
            name (str): A name for this person
        """
        self.moves = moves
        self.x = x_position
        self.y = y_position
        self.name = name

        self.can_jump = False
        self.jump_index = 0

        self.is_alive = True
        self.score = 0

        # The patter that the Geo People will jump. This person will go up for 2, wait for 2, and then down for 2
        self.jump_hash_map = {
            1: lambda y: y + 1,
            2: lambda y: y + 1,
            3: lambda y: y,
            4: lambda y: y,
            5: lambda y: y - 1,
        }

    def reset_geo(self, x_position:int, y_position:int):
        """A function to rest the Geo Person

        Args:
            x_position (int): The X position that the Geo Person will be on the board
            y_position (int): The starting Y position the Geo Person will be
                *NOTE* 0, is ideal, because then this is a moving object for someone to easily find and understand
        """
        self.x = x_position
        self.y = y_position

        self.can_jump = False
        self.jump_index = 0

        self.is_alive = True

    def _check_if_can_jump(self, board: List[str], board_state: int):
        """A hidden function to detect if the Geo Person is able to jump or not

        Args:
            board (List[str]): a list of strings which helps show the y axis of the board.
                *NOTE* Game runs for the length of the bottom of the map
            board_state (int): the X index of the board
        """
        self.can_jump = board[self.y + 1][board_state + self.x] == FLOOR_CHAR

    def check_if_is_alive(self, board: list, board_state: int):
        """A function to detect if the Geo Person is on a safe space, and if not then to mark them as dead

        Args:
            board (List[str]): a list of strings which helps show the y axis of the board.
                *NOTE* Game runs for the length of the bottom of the map
            board_state (int): the X index of the board
        """
        self.is_alive = board[self.y][board_state + self.x] == AIR_CHAR

    def move(self, board: list, board_state: int):
        """A function to adjust the y axis of the Geo Person for their given moves list

        Args:
            board (List[str]): a list of strings which helps show the y axis of the board.
                *NOTE* Game runs for the length of the bottom of the map
            board_state (int): the X index of the board
        """

        # checking to see if the geo person can jump
        self._check_if_can_jump(board=board, board_state=board_state)

        # if the geo person can jump
        if self.can_jump:
            # if the person chooses not to jump, our work here is done
            if self.moves[board_state] == 0:
                return

            # if the geo person chooses to jump, then we will decrease their Y value by 1, rising them up on the board
            self.y -= 1 if board[self.y - 1][board_state + self.x] == AIR_CHAR else 0
            # Dynamic-ness is important, we know how long we want the jump to be, and this code allows for the devs to
            # only have to update the self.jump_hash_map in the future, instead of referencing magic vars 
            self.jump_index = len(self.jump_hash_map)

            return

        # if the geo person can not jump, and they are currently jumping
        if self.jump_index > 0:
            # Checking to make sure that the geo person doesn't phase throw a ceiling, before updating
            desired_jump = self.jump_hash_map[self.jump_index](self.y)

            self.y = (
                desired_jump
                if board[desired_jump][board_state + self.x] == AIR_CHAR
                else self.y
            )

            self.jump_index -= 1
            return

        # if the geo person no not jump, and is not currently jumping... they are then falling
        self.y += 1
        return


def modify_moves(moves: List[int], modify_index: int) -> List[int]:
    """A function to create a new list of moves inspired by an existing list of moves

    Args:
        moves (List[int]): A list of 1's and 0's.
            1 = Jump
            0 = Don't Jump
        modify_index (int): An index to start changing the moves at. 
            *WARNING* Too small of an index and you may find your geos get stuck in a dead end

    Returns:
        List[int]: A list of 1's and 0's.
            1 = Jump
            0 = Don't Jump
    """
    # Making sure that modify index is always greater than equal to zero
    if modify_index < 0:
        modify_index = 0
    
    # itterating through the length of moves to modify and doing just that!
    for index in range(len(moves) - modify_index):
        if random.random() < EVOLUTION_CHANCE:
            moves[index + modify_index] = random.randint(0, 1)

    return moves
