from typing import List, Dict, Union
import random

EMPTY_TILE_ID = 0

HIT_UNSANK_SHIP_CODE = -2
UNHIT_CODE = 0
HIT_EMPTY_CODE = -1


class GameTile:
    def __init__(self, x_position: int, y_position: int, ship_id: int):
        """A class to represent a grid on the board

        Args:
            x_position (int): x position on the grid
            y_position (int): y position on the grid
            ship_id (int): an indicator of if tile is a ship or whiespace
        """
        self.x_position = x_position
        self.y_position = y_position
        self.ship_id = ship_id

        self.is_hit = False


class BattleshipGame:
    def __init__(self, size: int = 10):
        """A class to hold all of the gameplay mechanics for battleship

        Args:
            size (int, optional): the dimensions of the board, will always be a square. Defaults to 10.
        """
        self.size = size

        self.player_1_pieces = self.get_game_pieces()
        self.player_2_pieces = self.get_game_pieces()

        self.player_1_board = self.get_clear_board()
        self.player_2_board = self.get_clear_board()

    def fire_at_tile(self, opponent_id: int, x_position: int, y_position: int) -> bool:
        """A function to change the is_hit of a tile to false, and notify if a ship was hit!

        Args:
            opponent_id (int): the person fired at. 
                1 = Player 
                2 = AI
            x_position (int): the x location of the tile
            y_position (int): the y location of the tile

        Returns:
            bool: if the ship was hit or not
        """
        # Grabbing the needed fields according to the opponent_id
        # NOTE python doesn't have pointers, but referencing a nested object shares the memory!
        if opponent_id == 1:
            board = self.player_1_board
            player_pieces = self.player_1_pieces
        else:
            board = self.player_2_board
            player_pieces = self.player_2_pieces

        # Incase of missclics, we give the person back their turn
        if board[y_position][x_position].is_hit:
            return True
        
        # Toggling the tile to being hit
        board[y_position][x_position].is_hit = True

        # Checking if the tile was a ship
        ship_id = board[y_position][x_position].ship_id
        if ship_id == EMPTY_TILE_ID:
            return False

        # if the tile was a ship, updating to ship "is_sank" to see if all nested objects are hit
        player_pieces[ship_id]["is_sank"] = all(
            [tile.is_hit for tile in player_pieces[ship_id]["tiles"]]
        )

        return True


    """
    VALIDATORS
    ----------
    """
    def _is_valid_ship_location(
        self,
        player_id: int,
        x_position: int,
        y_position: int,
        ship_length: int,
        is_vertical: bool,
    ) -> bool:
        """A hidden function to validate that a ship can be placed on the board

        Args:
            player_id (int): the person who is setting the ship
            x_position (int): the top left ship x location
            y_position (int): the top left ship y location
            ship_length (int): how long the ship is
            is_vertical (bool): if the ship is along the x or y axis

        Returns:
            bool: _description_
        """
        # Grabbing the needed fields according to the opponent_id
        if player_id == 1:
            board = self.player_1_board
        else:
            board = self.player_2_board

        # Vertical check
        if is_vertical:
            # itterating over the range of vertical tiles
            for row in range(y_position, y_position + ship_length):
                # if the row is outside of the board bounds, or is a ship tile already
                if row >= self.size or board[row][x_position].ship_id != 0:
                    return False
            return True

        # Horizontal check
        # itterating over the column of vertical tiles
        for column in range(x_position, x_position + ship_length):
            # if the column is outside of the board bounds, or is a ship tile already
            if column >= self.size or board[y_position][column].ship_id != 0:
                return False
        return True

    """
    SETTERS
    -------
    """
    def _set_ship_location(
        self,
        player_id: int,
        ship_id: int,
        x_position: int,
        y_position: int,
        is_vertical: bool,
    ) -> bool:
        """A function to help set the position of a ship

        Args:
            player_id (int): the person who is setting the ship
            x_position (int): the top left ship x location
            y_position (int): the top left ship y location
            ship_length (int): how long the ship is
            is_vertical (bool): if the ship is along the x or y axis

        Returns:
            bool: if the ship was able to be set or not
        """
        # Grabbing the needed fields according to the opponent_id
        # NOTE python doesn't have pointers, but referencing a nested object shares the memory!
        if player_id == 1:
            board = self.player_1_board
            player_pieces = self.player_1_pieces
        else:
            board = self.player_2_board
            player_pieces = self.player_2_pieces

        # If the location is not a valid location, then we can not hit the ship
        if not self._is_valid_ship_location(
            player_id=player_id,
            x_position=x_position,
            y_position=y_position,
            ship_length=len(player_pieces[ship_id]["tiles"]),
            is_vertical=is_vertical,
        ):
            return False

        # if the location is valid, then we want to go across either the x or y axis and update the tiles to be the ship
        # NOTE similar to the comment before, since these are nested objects, python has a 'feature' which will treat them similar to a pointer
        if is_vertical:
            for row, ship_tile in zip(
                range(y_position, y_position + len(player_pieces[ship_id]["tiles"])),
                player_pieces[ship_id]["tiles"],
            ):
                board[row][x_position] = ship_tile
        else:
            for column, ship_tile in zip(
                range(x_position, x_position + len(player_pieces[ship_id]["tiles"])),
                player_pieces[ship_id]["tiles"],
            ):
                board[y_position][column] = ship_tile

        return True

    def set_random_board(self, player_id: int, seed: int = 0):
        """A function to create a board for the player

        Args:
            player_id (int): which player a board will be created for
            seed (int, optional): any time that there is randomness, a seed is always good so you can recreate results. Defaults to 0.
        """
        # Grabbing the needed fields according to the opponent_id
        # NOTE python doesn't have pointers, but referencing a nested object shares the memory!
        if player_id == 1:
            player_pieces = self.player_1_pieces
        else:
            player_pieces = self.player_2_pieces

        # Setting hte seed if there is one
        if seed:
            random.seed(seed)

        # itterating over all of the pieces and trying to set their location randomly
        for piece_id in player_pieces.keys():
            x_position, y_position, is_vertical = (
                random.randrange(0, self.size),
                random.randrange(0, self.size),
                bool(random.randrange(0, 2)),
            )
            while not self._set_ship_location(
                player_id=player_id,
                ship_id=piece_id,
                x_position=x_position,
                y_position=y_position,
                is_vertical=is_vertical,
            ):
                x_position, y_position, is_vertical = (
                    random.randrange(0, self.size),
                    random.randrange(0, self.size),
                    bool(random.randrange(0, 2)),
                )

    """
    GETTERS
    -------
    """
    def get_clear_board(self) -> List[List[GameTile]]:
        """A function to get the default board

        Returns:
            List[List[GameTile]]: will always be self.size X self.size
            [
                [ GameTile(space) , GameTile(space) , GameTile(space) ],
                [ GameTile(space) , GameTile(space) , GameTile(space) ],
                [ GameTile(space) , GameTile(space) , GameTile(space) ]
            ]
        """
        return [
            [
                GameTile(x_position=column, y_position=row, ship_id=EMPTY_TILE_ID)
                for column in range(self.size)
            ]
            for row in range(self.size)
        ]

    def get_game_pieces(self) -> Dict[int, Dict[str, Union[List[GameTile], bool]]]:
        """A function to get all of the pieces in the game

        Returns:
            Dict[int, Dict[str, Union[List[GameTile], bool]]]: all of the pieces in the game
                {
                    ship_id:{
                        tiles: [ GameTile(ship_id) ],
                        is_sank: bool
                    }
                }
        """
        return {
            1: {
                "tiles": [
                    GameTile(x_position=-1, y_position=-1, ship_id=1),
                    GameTile(x_position=-1, y_position=-1, ship_id=1),
                ],
                "is_sank": False,
            },
            2: {
                "tiles": [
                    GameTile(x_position=-1, y_position=-1, ship_id=2),
                    GameTile(x_position=-1, y_position=-1, ship_id=2),
                    GameTile(x_position=-1, y_position=-1, ship_id=2),
                ],
                "is_sank": False,
            },
            3: {
                "tiles": [
                    GameTile(x_position=-1, y_position=-1, ship_id=3),
                    GameTile(x_position=-1, y_position=-1, ship_id=3),
                    GameTile(x_position=-1, y_position=-1, ship_id=3),
                ],
                "is_sank": False,
            },
            4: {
                "tiles": [
                    GameTile(x_position=-1, y_position=-1, ship_id=4),
                    GameTile(x_position=-1, y_position=-1, ship_id=4),
                    GameTile(x_position=-1, y_position=-1, ship_id=4),
                    GameTile(x_position=-1, y_position=-1, ship_id=4),
                ],
                "is_sank": False,
            },
            5: {
                "tiles": [
                    GameTile(x_position=-1, y_position=-1, ship_id=5),
                    GameTile(x_position=-1, y_position=-1, ship_id=5),
                    GameTile(x_position=-1, y_position=-1, ship_id=5),
                    GameTile(x_position=-1, y_position=-1, ship_id=5),
                    GameTile(x_position=-1, y_position=-1, ship_id=5),
                ],
                "is_sank": False,
            },
        }

    def get_view_board_opponent(self, opponent_id: int) -> List[List[int]]:
        """A function to get a simple view of the opponents board. This is used mainly in the AI.
        This does not spoil the location. It just shows what has and hasn't been hit

        Args:
            opponent_id (int): the person who's board you want to get a summary of

        Returns:
            List[List[int]]: A board of what has and hasn't been hit. ex
                [
                    [ 0,  0, -1 ],
                    [ 0,  0,  0 ],
                    [ 0, -2,  0 ]
                ]
                -1 = hit, but nothing of value
                -2 = hit ship and not sank
        """
        # Grabbing the needed fields according to the opponent_id
        # NOTE python doesn't have pointers, but referencing a nested object shares the memory!
        if opponent_id == 1:
            board = self.player_1_board
            players_pieces = self.player_1_pieces
        else:
            board = self.player_2_board
            players_pieces = self.player_2_pieces

        def decision_map(
            tile: GameTile,
            players_pieces: Dict[int, Dict[str, Union[List[GameTile], bool]]],
        ) -> int:
            """A simple function to do some simple mapping for our list manipulation

            Args:
                tile (GameTile): the piece in question
                players_pieces (Dict[int, Dict[str, Union[List[GameTile], bool]]]): all of the player pieces

            Returns:
                int: the code for the limited view board
                    -1 = hit, but nothing of value
                    -2 = hit ship and not sank
            """
            # tile has not been targeted
            if not tile.is_hit:
                return UNHIT_CODE
            # tile has been targeted, but is a blank space
            if tile.ship_id == EMPTY_TILE_ID:
                return HIT_EMPTY_CODE
            # tile has been targeted, and is a sunken ship
            if players_pieces[tile.ship_id]["is_sank"]:
                return HIT_EMPTY_CODE
            # tile has been targeted, and is not a sunken ship
            return HIT_UNSANK_SHIP_CODE

        return [
            [decision_map(tile=tile, players_pieces=players_pieces) for tile in row]
            for row in board
        ]

    def get_view_board_self(self, player_id: int) -> List[List[int]]:
        """A function for debugging only, returns the ids of all of the pieces on the board

        Args:
            player_id (int): which player we want to view the board of

        Returns:
            List[List[int]]: the board with the tile ids. ex
                [
                    [ 0 0 0 ],
                    [ 1 0 0 ],
                    [ 1 0 0 ]
                ]
        """
        # Grabbing the needed fields according to the opponent_id
        # NOTE python doesn't have pointers, but referencing a nested object shares the memory!
        if player_id == 1:
            board = self.player_1_board
        else:
            board = self.player_2_board
        return [[tile.ship_id for tile in row] for row in board]
