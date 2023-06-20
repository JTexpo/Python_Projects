import time
import tkinter as tk
from tkinter import font

from main import minimax_mancala

class MancalaTkinterUI(tk.Tk):
    def __init__(
        self,
        reference_size: int = 10,
    ):
        super().__init__()

        self.reference_size = reference_size
        self.player = "N/A"
        self.ai = "N/A"

        self.board = {
            "top": [4, 4, 4, 4, 4, 4],
            "bottom": [4, 4, 4, 4, 4, 4],
            "top_score": 0,
            "bottom_score": 0,
        }

        self.player_1_goal_label_text = "{player}\n{points:0>2}\n"
        self.player_2_goal_label_text = "\n{points:0>2}\n{player}"
        self.whos_turn_value_label_text = "N/A"
        self.ais_chance_value_label_text = "N/A"
        self.how_many_pieces_held_value_label_text = "0"
        self.ai_difficulty = 1
        self.winning_confidence_mapping = {
            -6: "Terrible",
            -1: "Bad",
            3: "Possible",
            6: "Good",
            100: "Certain",
        }

        self.title("Mancala")

        self.font_large = font.Font(size=self.reference_size * 2)
        self.font_med = font.Font(size=self.reference_size)
        self.font_small = font.Font(size=self.reference_size // 2)
        """UI Layout

        Player 1 Button | Player 2 Button       Quit Button
        ---------------------------------------------------
        Game Statistics
        Who's Turn              :
        AI's Chance of Winning  :
        How Many Pieces Held    :

        AI Difficulty slider
        ---------------------------------------------------
        BOARD GOES HERE
        """

        # FRAMES
        # ------
        # We will need 3 frames, because our sketch above is divided into 3 sections

        self.button_selector_frame = tk.Frame(
            master=self,
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            relief=tk.SOLID,
        )
        self.game_statistics_frame = tk.Frame(
            master=self,
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            relief=tk.SOLID,
        )
        self.mancala_board_frame = tk.Frame(
            master=self,
            padx=self.reference_size,
            pady=self.reference_size,
            background="brown",
            relief=tk.SOLID,
        )

        self.button_selector_frame.grid(column=0, row=0, sticky="nsew")
        self.game_statistics_frame.grid(column=0, row=1, sticky="nsew")
        self.mancala_board_frame.grid(column=0, row=2, sticky="nsew")

        # BUTTON SELECTOR FRAME
        # ---------------------

        # With UI
        self.player_1_button = tk.Button(
            master=self.button_selector_frame,
            text="Play As Player 1",
            background="orange",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=self.font_med,
            command=lambda: self.choose_player(plyare_type=1),
        )

        self.player_2_button = tk.Button(
            master=self.button_selector_frame,
            text="Play As Player 2",
            background="green",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=self.font_med,
            command=lambda: self.choose_player(plyare_type=2),
        )

        self.quit_button = tk.Button(
            master=self.button_selector_frame,
            text="Quit",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=self.font_med,
            command=lambda: quit(),
        )

        self.player_1_button.grid(column=0, row=0, sticky="nsew")
        self.player_2_button.grid(column=1, row=0, sticky="nsew")
        self.quit_button.grid(column=2, row=0, sticky="nse")

        # GAME STATS FRAME
        # ----------------

        self.game_stats_label = tk.Label(
            master=self.game_statistics_frame,
            text="Game Stats",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=self.font_large,
        )
        self.whos_turn_label = tk.Label(
            master=self.game_statistics_frame,
            text="Who's Turn",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=self.font_med,
        )
        self.ais_chance_label = tk.Label(
            master=self.game_statistics_frame,
            text="AI's Chance of Winning",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=self.font_med,
        )
        self.how_many_pieces_held_label = tk.Label(
            master=self.game_statistics_frame,
            text="How Many Pieces Held",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=self.font_med,
        )
        self.difficulty_scale_label = tk.Label(
            master=self.game_statistics_frame,
            text="AI Difficulty Slider",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=self.font_large,
        )

        self.whos_turn_value_label = tk.Label(
            master=self.game_statistics_frame,
            text="N/A",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=self.font_med,
        )
        self.ais_chance_value_label = tk.Label(
            master=self.game_statistics_frame,
            text="N/A",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=self.font_med,
        )
        self.how_many_pieces_held_value_label = tk.Label(
            master=self.game_statistics_frame,
            text="0",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=self.font_med,
        )
        self.difficulty_scale = tk.Scale(
            master=self.game_statistics_frame,
            orient="horizontal",
            from_=1,
            to=5,
            tickinterval=1,
            font=self.font_med,
            command=self.adjust_ai_difficulty,
        )

        self.collen_divider_label_list = []
        for index in range(3):
            collen_divider_label = tk.Label(
                master=self.game_statistics_frame,
                text=":",
                padx=self.reference_size // 2,
                pady=self.reference_size // 2,
                font=self.font_med,
            )
            collen_divider_label.grid(column=1, row=1 + index)
            self.collen_divider_label_list.append(collen_divider_label)

        self.game_stats_label.grid(column=0, row=0, sticky="nsw")
        self.whos_turn_label.grid(column=0, row=1, sticky="nsw")
        self.ais_chance_label.grid(column=0, row=2, sticky="nsw")
        self.how_many_pieces_held_label.grid(column=0, row=3, sticky="nsw")

        self.whos_turn_value_label.grid(column=2, row=1, sticky="nsw")
        self.ais_chance_value_label.grid(column=2, row=2, sticky="nsw")
        self.how_many_pieces_held_value_label.grid(column=2, row=3, sticky="nsw")

        self.difficulty_scale_label.grid(column=0, row=4, sticky="nsw")
        self.difficulty_scale.grid(column=0, row=5, columnspan=3, sticky="nsew")

        # BOARD
        # -----

        self.player_1_goal_label = tk.Label(
            master=self.mancala_board_frame,
            text="P 1\n00\n",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=self.font_large,
            width=self.reference_size // 4,
        )
        self.player_2_goal_label = tk.Label(
            master=self.mancala_board_frame,
            text="\n00\nP 2",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=self.font_large,
            width=self.reference_size // 4,
        )

        self.mancala_button_list = []
        for row in range(2):
            for column in range(6):

                def choose_move_closure(location: str, tile: int):
                    return lambda: self.choose_move(location=location, tile=tile)

                mancala_button = tk.Button(
                    master=self.mancala_board_frame,
                    text="4",
                    padx=self.reference_size // 2,
                    pady=self.reference_size // 2,
                    font=self.font_large,
                    command=choose_move_closure(
                        location="top" if row == 0 else "bottom",
                        tile=5 - column if row == 0 else column,
                    ),
                    width=self.reference_size // 8,
                )

                mancala_button.grid(column=1 + column, row=row, sticky="nsew")

                self.mancala_button_list.append(mancala_button)

        self.player_1_goal_label.grid(column=0, row=0, rowspan=2, sticky="nsew")
        self.player_2_goal_label.grid(column=7, row=0, rowspan=2, sticky="nsew")

    def sync_backend_front_end(self):
        """A function to connect all of the back end fields to their front end interface"""
        self.whos_turn_value_label.config(text=self.whos_turn_value_label_text)
        self.ais_chance_value_label.config(text=self.ais_chance_value_label_text)
        self.how_many_pieces_held_value_label.config(
            text=self.how_many_pieces_held_value_label_text
        )

        self.player_1_goal_label.config(
            text=self.player_1_goal_label_text.format(
                player="You" if self.player == "top" else "AI",
                points=self.board["top_score"],
            )
        )
        self.player_2_goal_label.config(
            text=self.player_2_goal_label_text.format(
                player="You" if self.player == "bottom" else "AI",
                points=self.board["bottom_score"],
            )
        )

        for index, tile in enumerate(reversed(self.board["top"])):
            self.mancala_button_list[index].config(text=tile)

        for index, tile in enumerate(self.board["bottom"]):
            self.mancala_button_list[index + 6].config(text=tile)

    def adjust_ai_difficulty(self, value: int):
        """A function to allow for the user to adjust how far the minimax will go

        Args:
            value (int): value from the slider bar
        """
        self.ai_difficulty = value

    def choose_player(self, plyare_type: int):
        """A function to allow for the user to go either first or second

        Args:
            plyare_type (int): an indicator so we can re-use the same function for player 1 or 2
        """
        if plyare_type == 1:
            self.player = "top"
            self.ai = "bottom"
            self.whos_turn_value_label_text = "You"

        if plyare_type == 2:
            self.player = "bottom"
            self.ai = "top"
            self.whos_turn_value_label_text = "AI"

        self.board = {
            "top": [4, 4, 4, 4, 4, 4],
            "bottom": [4, 4, 4, 4, 4, 4],
            "top_score": 0,
            "bottom_score": 0,
        }

        self.sync_backend_front_end()

        # if we are going second, we want to let the ai make its move, else we'll be never able to play the game
        if plyare_type == 2:
            best_score, move = minimax_mancala(
                self.board, self.ai, self.ai, int(self.ai_difficulty)
            )
            self.move_pieces(self.ai, move)

    def choose_move(self, location: str, tile: int):
        """A function ontop of the buttons to allow for the player to select a move

        Args:
            location (str): "top" or "bottom"
            tile (int): the selected tile
        """
        if (
            not ("you" in self.whos_turn_value_label_text.lower())
            or (self.player != location)
            or (self.board[location][tile] == 0)
        ):
            return

        self.move_pieces(location, tile)

    def move_pieces(self, turn: str, tile: int):
        """
        A copy pasta of the move_pieces from the main.py. The only difference, is that this has less dependency injection and references to values inside the class
        """
        pieces = self.board[turn][tile]
        self.board[turn][tile] = 0
        location = turn
        go_again = False

        # 2. Moving counter-clockwise, the player deposits one of the stones in each pocket until the stones run out.
        while pieces > 0:
            self.how_many_pieces_held_value_label_text = pieces
            self.sync_backend_front_end()
            self.update()
            time.sleep(0.2)

            go_again = False
            pieces -= 1
            tile += 1

            if tile < len(self.board[location]):
                self.board[location][tile] += 1
                continue

            # 3. If you run into your own Mancala (store), deposit one piece in it.
            # If you run into your opponent's Mancala, skip it and continue moving to the next pocket.
            # 4. If the last piece you drop is in your own Mancala, you take another turn.
            if location == turn:
                self.board[f"{turn}_score"] += 1
                go_again = True
            else:
                pieces += 1

            location = "bottom" if location == "top" else "top"
            tile = -1

        self.how_many_pieces_held_value_label_text = 0
        self.sync_backend_front_end()
        time.sleep(0.2)

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
            and (self.board[location][tile] == 1)
            and (
                self.board[inverse_location][
                    len(self.board[inverse_location]) - 1 - tile
                ]
                != 0
            )
        ):
            self.board[f"{turn}_score"] += (
                1
                + self.board[inverse_location][
                    len(self.board[inverse_location]) - 1 - tile
                ]
            )
            self.board[location][tile] = 0
            self.board[inverse_location][
                len(self.board[inverse_location]) - 1 - tile
            ] = 0

        # 7. The game ends when all six pockets on one side of the Mancala board are empty.
        # 8. The player who still has pieces on his/her side of the board when the game ends captures all of those pieces.
        if (not any(self.board["top"])) or (not any(self.board["bottom"])):
            self.board["top_score"] += sum(self.board["top"])
            self.board["bottom_score"] += sum(self.board["bottom"])

            self.board["top"] = [0] * len(self.board["top"])
            self.board["bottom"] = [0] * len(self.board["bottom"])
            self.whos_turn_value_label_text = "Game Over"
            self.sync_backend_front_end()
            go_again = False
            return

        if not go_again:
            self.whos_turn_value_label_text = (
                "You" if self.whos_turn_value_label_text == "AI" else "AI"
            )

        self.sync_backend_front_end()

        if self.whos_turn_value_label_text == "AI":
            best_score, move = minimax_mancala(
                self.board, self.ai, self.ai, int(self.ai_difficulty)
            )
            for score, confidence in self.winning_confidence_mapping.items():
                if score < best_score:
                    continue
                self.ais_chance_value_label_text = confidence
                break
            self.move_pieces(self.ai, move)

def main():
    mancala = MancalaTkinterUI(14)
    mancala.mainloop()

if __name__ == "__main__":
    main()
