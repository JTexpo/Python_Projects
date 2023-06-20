from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
from tkinter import font
from typing import List
import time

import ai
from game import BattleshipGame, EMPTY_TILE_ID


class BattleshipGUI(tk.Tk):
    def __init__(self, battleship: BattleshipGame, reference_size: int):
        super().__init__()

        # Some deafault inits that we will need for the UI
        self.reference_size = reference_size
        self.battleship = battleship
        self.title("Battleship AI")

        # 3 size font tags. NOT ALL USED
        self.font_large = font.Font(size=self.reference_size * 2)
        self.font_med = font.Font(size=self.reference_size * 8)
        self.font_small = font.Font(size=self.reference_size // 2)

        # A mapping of all of our images for the board
        self.image_dict = {
            "water": ImageTk.PhotoImage(
                Image.open("./images/water.jpeg")
                .convert("RGB")
                .resize(size=(self.reference_size, self.reference_size))
            ),
            "water_hit": ImageTk.PhotoImage(
                Image.open("./images/water_hit.jpeg")
                .convert("RGB")
                .resize(size=(self.reference_size, self.reference_size))
            ),
            "ship": ImageTk.PhotoImage(
                Image.open("./images/ship.jpeg")
                .convert("RGB")
                .resize(size=(self.reference_size, self.reference_size))
            ),
            "ship_hit": ImageTk.PhotoImage(
                Image.open("./images/ship_hit.jpeg")
                .convert("RGB")
                .resize(size=(self.reference_size, self.reference_size))
            ),
            # TKinter doesnt do paddinf for labels on mac, so the size is scaled to be slightly bigger for the player
            "water_big": ImageTk.PhotoImage(
                Image.open("./images/water.jpeg")
                .convert("RGB")
                .resize(
                    size=(
                        int(self.reference_size * 1.2),
                        int(self.reference_size * 1.2),
                    )
                )
            ),
            "water_hit_big": ImageTk.PhotoImage(
                Image.open("./images/water_hit.jpeg")
                .convert("RGB")
                .resize(size=(self.reference_size, self.reference_size))
            ),
            "ship_big": ImageTk.PhotoImage(
                Image.open("./images/ship.jpeg")
                .convert("RGB")
                .resize(
                    size=(
                        int(self.reference_size * 1.2),
                        int(self.reference_size * 1.2),
                    )
                )
            ),
            "ship_hit_big": ImageTk.PhotoImage(
                Image.open("./images/ship_hit.jpeg")
                .convert("RGB")
                .resize(size=(self.reference_size, self.reference_size))
            ),
        }

        # What I hopefully want the board to look like
        """
        New Game
        +---------------+
        |               |
        |  Enemy View   +---------------+
        |               |               |
        +---------------+   AI Moves    |
        |               |               |
        |   Your View   +---------------+
        |               |
        +---------------+
        """

        # FRAMES
        # ------
        
        # self nested frames
        self.game_play_frame = tk.Frame(
            master=self,
            padx=self.reference_size // 4,
            pady=self.reference_size // 4,
            relief=tk.SOLID,
        )
        self.ai_view_frame = tk.Frame(
            master=self,
            padx=self.reference_size // 4,
            pady=self.reference_size // 4,
            relief=tk.SOLID,
        )
        self.reset_button = tk.Button(
            master=self, font=self.font_small, text="Reset Game", command=self.reset
        )

        self.reset_button.grid(column=0, row=0, sticky="nsw")
        self.game_play_frame.grid(column=0, row=1)
        self.ai_view_frame.grid(column=1, row=1)

        # gameplay nested frames
        self.enemy_view_frame = tk.Frame(
            master=self.game_play_frame,
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            relief=tk.SOLID,
        )
        self.player_view_frame = tk.Frame(
            master=self.game_play_frame,
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            relief=tk.SOLID,
        )
        self.enemy_view_label = tk.Label(
            master=self.game_play_frame, font=self.font_small, text="Enemy Tile Select"
        )
        self.player_view_label = tk.Label(
            master=self.game_play_frame, font=self.font_small, text="Your Tile Select"
        )

        self.enemy_view_label.grid(column=0, row=0)
        self.enemy_view_frame.grid(column=0, row=1)
        self.player_view_label.grid(column=0, row=2)
        self.player_view_frame.grid(column=0, row=3)

        # ENEMY VIEW FRAME
        # ----------------
        self.enemy_view_buttons: List[tk.Button] = []
        # itterating over all of the board length and creating buttons linked to the grid size
        for row in range(self.battleship.size):
            for column in range(self.battleship.size):
                
                # A function to help allow for a button to refrence a command, but with a changing var
                # NOTE. just using the lambda would place a reference on the button, that is why we have this closure
                def fire_closure(x_position: int, y_position: int):
                    return lambda: self.fire(
                        x_position=x_position, y_position=y_position
                    )

                # Creating a button of the tile and adding it to the main list
                _button = tk.Button(
                    master=self.enemy_view_frame,
                    image=self.image_dict["water"],
                    command=fire_closure(x_position=column, y_position=row),
                )
                _button.grid(column=column, row=row)
                self.enemy_view_buttons.append(_button)

        # PLAYER VIEW FRAME
        # -----------------
        self.player_view_game_labels: List[tk.Label] = []
         # itterating over all of the board length and creating label linked to the grid size
        for row in range(self.battleship.size):
            for column in range(self.battleship.size):
                 # Creating a label of the tile and adding it to the main list
                _label = tk.Label(
                    master=self.player_view_frame,
                    image=self.image_dict["water_big"]
                    if self.battleship.player_1_board[row][column].ship_id
                    == EMPTY_TILE_ID
                    else self.image_dict["ship_big"],
                )
                _label.grid(column=column, row=row)
                self.player_view_game_labels.append(_label)

        # AI VIEW FRAME
        # -------------
        self.graph_figure = Figure(
            figsize=(
                self.reference_size,
                self.reference_size,
            ),
            dpi=self.reference_size,
        )
        self.graph_canvas = FigureCanvasTkAgg(
            master=self.ai_view_frame, figure=self.graph_figure
        )
        self.subplot = self.graph_figure.add_subplot(111)

        # Grabbing the initial AI best moves
        ai_heat_map_board, _, _ = ai.find_best_move(
            board=self.battleship.get_view_board_opponent(opponent_id=1),
            ship_lengths=[
                len(ship["tiles"])
                for ship_id, ship in self.battleship.player_1_pieces.items()
                if not ship["is_sank"]
            ],
        )

        # creating a heatmap of what the AI thinks are the best moves
        self.heatmap = self.subplot.imshow(
            ai_heat_map_board, cmap="hot_r", interpolation="nearest"
        )
        self.cbar = self.graph_figure.colorbar(self.heatmap)
        self.cbar.set_label(
            "AI Moves Confidence (heatmap)",
            fontsize=self.reference_size * 2,
            rotation=270,
            labelpad=self.reference_size * 2,
        )
        self.subplot.figure.set_facecolor("gray")
        self.subplot.figure.suptitle("AI Move View", fontsize=self.reference_size * 4)
        self.subplot.tick_params(axis="x", labelsize=self.reference_size * 2)
        self.subplot.tick_params(axis="y", labelsize=self.reference_size * 2)

        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack()

        return

    def update_backend_to_frontend(self):
        """A function to connect all of the GUI with what works behind scenes
        """
        # itterating over the board and updating the buttons and labels
        for row in range(self.battleship.size):
            for column in range(self.battleship.size):

                # Updating the players labels
                if self.battleship.player_1_board[row][column].is_hit:
                    self.player_view_game_labels[
                        column + (row * self.battleship.size)
                    ].config(
                        image=self.image_dict["water_hit_big"]
                        if self.battleship.player_1_board[row][column].ship_id
                        == EMPTY_TILE_ID
                        else self.image_dict["ship_hit_big"]
                    )
                else:
                    self.player_view_game_labels[
                        column + (row * self.battleship.size)
                    ].config(
                        image=self.image_dict["water_big"]
                        if self.battleship.player_1_board[row][column].ship_id
                        == EMPTY_TILE_ID
                        else self.image_dict["ship_big"]
                    )
                 # Updating the enemys buttons
                if self.battleship.player_2_board[row][column].is_hit:
                    self.enemy_view_buttons[
                        column + (row * self.battleship.size)
                    ].config(
                        image=self.image_dict["water_hit"]
                        if self.battleship.player_2_board[row][column].ship_id
                        == EMPTY_TILE_ID
                        else self.image_dict["ship_hit"]
                    )
                else:
                    self.enemy_view_buttons[
                        column + (row * self.battleship.size)
                    ].config(image=self.image_dict["water"])

        # Clear existing graph
        self.subplot.clear()

        # Grabbing the AI best moves
        ai_heat_map_board, _, _ = ai.find_best_move(
            board=self.battleship.get_view_board_opponent(opponent_id=1),
            ship_lengths=[
                len(ship["tiles"])
                for ship_id, ship in self.battleship.player_1_pieces.items()
                if not ship["is_sank"]
            ],
        )
        self.heatmap = self.subplot.imshow(
            ai_heat_map_board, cmap="hot_r", interpolation="nearest"
        )
        self.subplot.figure.set_facecolor("gray")
        self.subplot.figure.suptitle("AI Move View", fontsize=self.reference_size * 4)
        self.subplot.tick_params(axis="x", labelsize=self.reference_size * 2)
        self.subplot.tick_params(axis="y", labelsize=self.reference_size * 2)
        self.graph_canvas.draw()

        # Updating the tkinter UI
        self.update()

    def fire(self, x_position: int, y_position: int):
        """A function for the players buttons to fire at a enemy tile

        Args:
            x_position (int): the x location of the button
            y_position (int): the y location of the button
        """

        # Firing at the ship!
        did_hit = self.battleship.fire_at_tile(
            opponent_id=2, x_position=x_position, y_position=y_position
        )

        # Updating the board, now that the player selected a tile
        self.update_backend_to_frontend()

        # if the player did not hit, then it is the AI's turn
        if not did_hit:

            # Grabbing the AI's move
            _, ai_x_move, ai_y_move = ai.find_best_move(
                board=self.battleship.get_view_board_opponent(opponent_id=1),
                ship_lengths=[
                    len(ship["tiles"])
                    for ship_id, ship in self.battleship.player_1_pieces.items()
                    if not ship["is_sank"]
                ],
            )

            # While the AI keeps hitting the player, we want to update the board and continue on with the next move
            while self.battleship.fire_at_tile(
                opponent_id=1, x_position=ai_x_move, y_position=ai_y_move
            ):
                self.update_backend_to_frontend()
                _, ai_x_move, ai_y_move = ai.find_best_move(
                    board=self.battleship.get_view_board_opponent(opponent_id=1),
                    ship_lengths=[
                        len(ship["tiles"])
                        for ship_id, ship in self.battleship.player_1_pieces.items()
                        if not ship["is_sank"]
                    ],
                )
                # small sleep so this doesnt happen all at once
                time.sleep(0.5)

            self.update_backend_to_frontend()

        return

    def reset(self):
        """A function for if a new game is wanted to be played
        """
        self.battleship = BattleshipGame(self.battleship.size)
        self.battleship.set_random_board(player_id=1)
        self.battleship.set_random_board(player_id=2)
        self.update_backend_to_frontend()

def main():
    game = BattleshipGame(size=10)
    game.set_random_board(player_id=1, seed=4)
    game.set_random_board(player_id=2, seed=1)

    gui = BattleshipGUI(battleship=game, reference_size=24)
    gui.mainloop()

if __name__ == "__main__":
    main()