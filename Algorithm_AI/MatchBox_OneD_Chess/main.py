"""One D Chess Rules

Board
+------------+--------------+------------+------+------+------------+--------------+------------+
| White King | White Knight | White Rook |      |      | Black Rook | Black Knight | Black King |
+------------+--------------+------------+------+------+------------+--------------+------------+

Goal, you play as white and need to get the king in checkmate! 
Getting checkmatted yourself is a loss, along with stalemate

One D Chess Alternate Piece Move :
Unlike in normal chess, the knight moves 2 spaces, and can hop over a piece. ( Regular Knight Movement - Left / Right )
"""
from PIL import Image, ImageTk

import tkinter as tk
from tkinter import font
import time

from chessBoard import (
    Board,
    WHITE_TEAM_ID,
    BLACK_TEAM_ID,
    KING_PIECE_ID,
    KNIGHT_PIECE_ID,
    ROOK_PIECE_ID,
    NULL_TEAM_ID,
    SPACE_PIECE_ID,
)
from utils import train


class OneDChess(tk.Tk):
    def __init__(self, reference_size: int):
        """ The GUI for OneDChess

        Args:
            reference_size int: A size to base the spacing and text around
        """
        # Tkinter init
        super().__init__()
        self.reference_size = reference_size
        self.title("One-D Chess AI")
        self.font_large = font.Font(size=self.reference_size * 2)
        self.font_med = font.Font(size=self.reference_size * 8)
        self.font_small = font.Font(size=self.reference_size // 2)
        self.image_dict = {
            f"{WHITE_TEAM_ID}{KING_PIECE_ID}": ImageTk.PhotoImage(
                Image.open("./images/white_king.png").convert("RGB")
            ),
            f"{WHITE_TEAM_ID}{KNIGHT_PIECE_ID}": ImageTk.PhotoImage(
                Image.open("./images/white_knight.png").convert("RGB")
            ),
            f"{WHITE_TEAM_ID}{ROOK_PIECE_ID}": ImageTk.PhotoImage(
                Image.open("./images/white_rook.png").convert("RGB")
            ),
            f"{BLACK_TEAM_ID}{KING_PIECE_ID}": ImageTk.PhotoImage(
                Image.open("./images/black_king.png").convert("RGB")
            ),
            f"{BLACK_TEAM_ID}{KNIGHT_PIECE_ID}": ImageTk.PhotoImage(
                Image.open("./images/black_knight.png").convert("RGB")
            ),
            f"{BLACK_TEAM_ID}{ROOK_PIECE_ID}": ImageTk.PhotoImage(
                Image.open("./images/black_rook.png").convert("RGB")
            ),
            f"{NULL_TEAM_ID}{SPACE_PIECE_ID}": ImageTk.PhotoImage(
                Image.open("./images/space.png").convert("RGB")
            ),
        }
        # Backend init
        self.selected_move = -1
        self.turn_value_text = "N/A"
        self.selected_piece_value_text = "N/A"
        self.game_board = Board()
        self.AI_MOVES = train()

        """
        RESET BUTTON
        turn : ___
        selected piece : ___
        ---------
        BOARD
        """

        # FRAMES
        # ------
        self.game_details_frame = tk.Frame(
            master=self,
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            relief=tk.SOLID,
        )

        self.board_frame = tk.Frame(
            master=self,
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            relief=tk.SOLID,
        )

        self.game_details_frame.grid(column=0, row=0, sticky="NSW")
        self.board_frame.grid(column=0, row=1)

        # GAME DETAILS FRAME
        # ------------------

        self.reset_button = tk.Button(
            master=self.game_details_frame,
            text="Reset Board",
            font=self.font_med,
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            command=self.reset_board,
        )

        self.turn_label = tk.Label(
            master=self.game_details_frame,
            text="Turn",
            font=self.font_med,
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
        )

        self.selected_piece_label = tk.Label(
            master=self.game_details_frame,
            text="Selected Piece",
            font=self.font_med,
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
        )

        self.collen_divider_label_list = []
        for index in range(2):
            collen_divider_label = tk.Label(
                master=self.game_details_frame,
                text=":",
                padx=self.reference_size // 2,
                pady=self.reference_size // 2,
                font=self.font_med,
            )
            collen_divider_label.grid(column=1, row=1 + index)
            self.collen_divider_label_list.append(collen_divider_label)

        self.turn_value_label = tk.Label(
            master=self.game_details_frame,
            text="AI (White)",
            font=self.font_med,
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
        )

        self.selected_piece_value_label = tk.Label(
            master=self.game_details_frame,
            text="N/A",
            font=self.font_med,
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
        )

        self.reset_button.grid(column=0, row=0, sticky="NSW")
        self.turn_label.grid(column=0, row=1, sticky="NSW")
        self.turn_value_label.grid(column=2, row=1, sticky="NSW")
        self.selected_piece_label.grid(column=0, row=2, sticky="NSW")
        self.selected_piece_value_label.grid(column=2, row=2, sticky="NSW")

        # BOARD
        # -----

        self.board_button_list = []

        for index, piece in enumerate(self.game_board.board):

            def select_move_closure(index: int):
                return lambda: self.select_move(index=index)

            _piece_button = tk.Button(
                master=self.board_frame,
                padx=self.reference_size // 2,
                pady=self.reference_size // 2,
                image=self.image_dict.get(f"{piece.team_id}{piece.piece_id}"),
                command=select_move_closure(index),
            )
            _piece_button.grid(column=index, row=0)
            self.board_button_list.append(_piece_button)

        time.sleep(0.5)
        self._ai_move()

    def reset_board(self):
        """A function to reset the board and tell the AI to go first
        """
        self.game_board.reset_board()

        self._sync_gui()
        time.sleep(0.5)
        self._ai_move()

    def _update_buttons(self):
        """A function to sync the buttons with the backend values
        """
        for index, piece in enumerate(self.game_board.board):
            self.board_button_list[index].config(
                image=self.image_dict.get(f"{piece.team_id}{piece.piece_id}")
            )

        self.update()

    def _sync_gui(self):
        """A function to sync the backend with the frontend
        """
        self._update_buttons()

        self.turn_value_label.config(text=self.turn_value_text)
        self.selected_piece_value_label.config(text=self.selected_piece_value_text)

        self.update()

    def _ai_move(self):
        """A function to grab the AI's move and update accordingly
        """
        move = self.AI_MOVES[self.game_board.get_string_board()][0]
        self.game_board.move_pieces(start=move["start"], end=move["end"])

        self.turn_value_text = "You (Black)"
        self.selected_piece_value_text = f"N/A"
        self.selected_move = -1

        self._sync_gui()

    def select_move(self, index: int):
        """A function to get the players move

        Args:
            index (int): the tile the player selected
        """
        # if the player reclicks on the piece, they are putting it down
        if (index == self.selected_move):
            self.selected_move = -1
            self.turn_value_text = "You (Black)"
            self.selected_piece_value_text = f"N/A"
            self._sync_gui()
            return
        # if the player has not selected a piece, and the piece they clicked on is a black team piece. Pick up the piece
        if (self.selected_move == -1) and (
            self.game_board.board[index].team_id == BLACK_TEAM_ID
        ):
            self.selected_move = index

            self.turn_value_text = "You (Black)"
            self.selected_piece_value_text = (
                f"{index} : {self.game_board.board[index].name}"
            )

            self._sync_gui()
            return
        # if they selected a piece that is not on their team to pick up
        if self.selected_move == -1:
            return
        # if the player is holding one of their pieces and they select on a valid move
        if self.game_board.validate_move(start=self.selected_move, end=index):
            self.game_board.move_pieces(start=self.selected_move, end=index)
            self.selected_move = -1

            self.turn_value_text = "AI (White)"
            self.selected_piece_value_text = f"N/A"
            self._sync_gui()
            time.sleep(0.5)
            self._ai_move()


if __name__ == "__main__":
    game = OneDChess(10)
    game.mainloop()