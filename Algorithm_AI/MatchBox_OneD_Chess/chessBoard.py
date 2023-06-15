from typing import List

# *NOTE* PLEASE KEEP THIS NUMBER EVEN
MAX_GAME_LENGTH = 20

NULL_TEAM_ID = 0
WHITE_TEAM_ID = 1
BLACK_TEAM_ID = 2

SPACE_PIECE_ID = 0
KING_PIECE_ID = 1
KNIGHT_PIECE_ID = 2
ROOK_PIECE_ID = 3


class ChessPiece:
    def __init__(self, name: str, team_id: int, piece_id: int):
        """A struct for the pieces

        Args:
            name (str): String (GUI use only)
            team_id (int): references what team the piece is on :
                NULL_TEAM_ID = 0
                WHITE_TEAM_ID = 1
                BLACK_TEAM_ID = 2
            piece_id (int): references what piece this piece is :
                SPACE_PIECE_ID = 0
                KING_PIECE_ID = 1
                KNIGHT_PIECE_ID = 2
                ROOK_PIECE_ID = 3
        """
        self.name = name
        self.team_id = team_id
        self.piece_id = piece_id


class Board:
    def __init__(self):
        """A list of the pieces which holds functions such as validation"""
        self.board = self._get_new_board()

    def _get_new_board(self) -> List[ChessPiece]:
        """Resetting the board

        Returns:
            List[ChessPiece]: _description_
        """
        return [
            # Whites Side
            ChessPiece(name="King", team_id=WHITE_TEAM_ID, piece_id=KING_PIECE_ID),
            ChessPiece(name="Knight", team_id=WHITE_TEAM_ID, piece_id=KNIGHT_PIECE_ID),
            ChessPiece(name="Rook", team_id=WHITE_TEAM_ID, piece_id=ROOK_PIECE_ID),
            # Spaces
            ChessPiece(name="space", team_id=NULL_TEAM_ID, piece_id=SPACE_PIECE_ID),
            ChessPiece(name="space", team_id=NULL_TEAM_ID, piece_id=SPACE_PIECE_ID),
            # Blacks Side
            ChessPiece(name="Rook", team_id=BLACK_TEAM_ID, piece_id=ROOK_PIECE_ID),
            ChessPiece(name="Knight", team_id=BLACK_TEAM_ID, piece_id=KNIGHT_PIECE_ID),
            ChessPiece(name="King", team_id=BLACK_TEAM_ID, piece_id=KING_PIECE_ID),
        ]

    def _get_space_class(self) -> ChessPiece:
        """A function to get the space chess piece

        Returns:
            ChessPiece: A space chess piece
        """
        return ChessPiece(name="space", team_id=NULL_TEAM_ID, piece_id=SPACE_PIECE_ID)

    def _validate_rook_move(self, start: int, end: int) -> bool:
        """A function to detect if a rook move is legal

        Args:
            start (int): rook's starting position
            end (int): where the rook would like to go

        Returns:
            bool: if the move is valid or not
        """

        # Making a copy of the board, so we can edit and not mess up current game
        board_copy = self.board.copy()

        # Checking to make sure that the rook is not capturing a piece on their team
        if self.board[start].team_id == self.board[end].team_id:
            return False

        # Setting start and end to empty
        board_copy[start] = self._get_space_class()
        board_copy[end] = self._get_space_class()

        # Logic to handel moving both left and right
        if start < end:
            return not sum([tile.piece_id for tile in board_copy[start:end]])
        elif start > end:
            return not sum([tile.piece_id for tile in board_copy[end:start]])

        # We should only reach this if start == end,
        # and that will be false, because you can not choose to not move
        return False

    def _validate_knight_move(self, start: int, end: int) -> bool:
        """A function to detect if a knights move is legal

        Args:
            start (int): knights's starting position
            end (int): where the knights would like to go

        Returns:
            bool: if the move is valid or not
        """
        # Checking to make sure that the rook is not capturing a piece on their team
        if self.board[start].team_id == self.board[end].team_id:
            return False

        # The knight can only move 2 spaces forward and backwards
        return abs(start - end) == 2

    def _validate_king_move_no_check_check(self, start: int, end: int) -> bool:
        """A function to detect if a a king is able to be captured by another king

        Args:
            start (int): kings starting position
            end (int): where the kings would like to go

        Returns:
            bool: if the move is valid or not
        """
        # Checking to make sure that the rook is not capturing a piece on their team
        if self.board[start].team_id == self.board[end].team_id:
            return False

        # The knight can only move 1 spaces forward and backwards
        return abs(start - end) == 1

    def _validate_king_move(self, start: int, end: int) -> bool:
        """A function to detect if a Kings move is legal

        Args:
            start (int): kings's starting position
            end (int): where the king would like to go

        Returns:
            bool: if the move is valid or not
        """
        # Checking to make sure that the rook is not capturing a piece on their team
        if self.board[start].team_id == self.board[end].team_id:
            return False

        # The knight can only move 1 spaces forward and backwards
        if abs(start - end) != 1:
            return False

        board_copy = self.board.copy()
        validate_hash_map = {
            ROOK_PIECE_ID: self._validate_rook_move,
            KNIGHT_PIECE_ID: self._validate_knight_move,
            # this helps break inf recursion of kings checking if one another can put them in check
            KING_PIECE_ID: self._validate_king_move_no_check_check,
        }

        # updating the move
        self.board[start] = self._get_space_class()
        self.board[end] = self.board[start]

        # Grabbing the opposed team, inverse of what our current team is
        opposed_team = (
            BLACK_TEAM_ID
            if self.board[start].team_id == WHITE_TEAM_ID
            else WHITE_TEAM_ID
        )

        for tile_index, tile_piece in enumerate(board_copy):
            # no friendly fire!
            if opposed_team != tile_piece.team_id:
                continue

            # Checking to see if any piece can reach the king on the new tile, and if so then returning false
            if validate_hash_map.get(
                tile_piece.piece_id, lambda *args, **kwargs: False
            )(start=tile_index, end=end):
                self.board = board_copy.copy()
                return False

        self.board = board_copy.copy()
        # no pieces are threatening the chosen tile
        return True

    def _detect_king_is_checked(self, team_id: int, inside_recursion: int = 0) -> bool:
        """A function to check the board and see if the king is checked

        Args:
            team_id (int): _description_
            inside_recursion (bool, optional): _description_. Defaults to False.

        Returns:
            bool: _description_
        """
        # Finding the current teams king location
        king_location = -1
        for tile_index, tile_piece in enumerate(self.board):
            if tile_piece.piece_id == 1 and tile_piece.team_id == team_id:
                king_location = tile_index
                break

        # this should never occure, but if the king is not found then return that the king is in check
        if king_location == -1:
            return True

        # itterating through the enemy moves
        for tile_index, tile_piece in enumerate(self.board):
            if tile_piece.team_id == team_id:
                continue

            # Checking if the enemy piece can reach the king without placing themself in check
            # WARNING :
            # Validate Move calls Detect King Is Check!!! this is back and forth recursion, and while python can handle it, we should also add in spedical logic
            if self.validate_move(
                start=tile_index, end=king_location, inside_recursion=inside_recursion
            ):
                return True

        # king is all safe
        return False

    def get_string_board(self) -> str:
        """Getting a string state of the board for the AI

        Returns:
            str: a string view of the board
        """
        return "_".join([f"{piece.team_id}{piece.piece_id}" for piece in self.board])

    def move_pieces(self, start: int, end: int) -> None:
        """assigning one piece to another location

        Args:
            start (int): piece to move starting index
            end (int): piece to move ending index
        """
        piece = self.board[start]

        self.board[start] = self._get_space_class()
        self.board[end] = piece

    def reset_board(self) -> None:
        """setting the board to what it was init to"""
        self.board = self._get_new_board()

    def validate_move(self, start: int, end: int, inside_recursion: int = 0) -> bool:
        """A function to validate that a move is a legal move

        Args:
            start (int): the pieces location
            end (int): the pieces destination
            inside_recursion (int, optional): a flag to know if we are inside of recursion for too long. Defaults to 0.

        Returns:
            bool: _description_
        """

        # A function to break too far recursion
        if inside_recursion > 10:
            return False

        piece_id = self.board[start].piece_id
        team_id = self.board[start].team_id

        validate_hash_map = {
            ROOK_PIECE_ID: self._validate_rook_move,
            KNIGHT_PIECE_ID: self._validate_knight_move,
            KING_PIECE_ID: self._validate_king_move,
        }

        # Checking to make sure that the rook is not capturing a piece on their team
        if team_id == self.board[end].team_id:
            return False

        # checking if the move is a legal move
        is_valid_move = validate_hash_map.get(piece_id, lambda *args, **kwargs: False)(
            start=start, end=end
        )

        if not is_valid_move:
            return False

        # Checking if the move places te king into check, making it not a legal move
        board_copy = self.board.copy()

        self.move_pieces(start=start, end=end)
        # WARNING :
        # Validate Move calls Detect King Is Check!!! this is back and forth recursion, and while python can handle it, we should also add in spedical logic
        is_king_checked = self._detect_king_is_checked(
            team_id=team_id, inside_recursion=inside_recursion + 1
        )

        # after the board has been updated and played with we can now set it back to its default self
        if not inside_recursion:
            self.board = board_copy.copy()

        return not is_king_checked
