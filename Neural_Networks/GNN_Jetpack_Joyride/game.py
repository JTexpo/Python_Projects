from pygame import display, event, time, Surface, sprite, font, QUIT
from pygame import quit as pygame_quit
from pygame import init as pygame_init
import pygame

from typing import List
import random

from game_objects.background import Background
from game_objects.coin import Coin
from game_objects.player import Player
from game_objects.zapper import Zapper

from neural_network import NeuralNetwork

AI_VISION_BOLD = 10
BOUND_RATIO = 5
FONT_RATIO = 20
ROTATE_LOWER = -90
ROTATE_UPPER = 90
TEXT_X_RATIO = 4
TEXT_BOARDER = 10

class AIGame:
    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        fps: int,
        screen_delta: int,
        ais: List[NeuralNetwork],
        zapper_spacing: int,
        coin_spacing: int,
        alive_reward: int,
        coin_reward: int,
        complete_reward: int,
    ):
        """The Jetpack Joyride game, for GNN AI models to interact with

        Args:
            screen_width (int): how wide the screen is
            screen_height (int): how tall the screen is
            fps (int): how fast the screen will update
            screen_delta (int): how fast will the game objects move
            ais (List[NeuralNetwork]): a list of all of the Neural Networks to play the game
            zapper_spacing (int): the delta between the zappers
            coin_spacing (int): the delta between the coins
            alive_reward (int): an award to be given every frame the AI is alive for
            coin_reward (int): an award to be given when the AI collects a coin
            complete_reward (int): an award to be given for completing the game
        """
        # Need to init pygames before anything else
        pygame_init()

        # Storing all inputs into class varibles to be called later
        self.window_width = screen_width
        self.window_height = screen_height
        self.fps = fps
        self.screen_delta = screen_delta
        self.ais = ais
        self.zapper_spacing = zapper_spacing
        self.coin_spacing = coin_spacing
        self.alive_reward = alive_reward
        self.coin_reward = coin_reward
        self.complete_reward = complete_reward

        # Creating the window as well as a game clock
        self.window = display.set_mode((self.window_width, self.window_height))
        display.set_caption("Jetpack Joyride AI")
        self.clock = time.Clock()
        self.stats_font = font.SysFont("arial", self.window_height // FONT_RATIO)

        # Creating bounds for where to spawn the coins and zappers in
        self.lower_spawn_bound = self.window_height // BOUND_RATIO
        self.upper_spawn_bound = self.window_height - self.window_height // BOUND_RATIO

    def init_game_objects(self):
        """A function to place all of the objects on the board. This can be used as a set / reset to the game"""

        # BACKGROUND
        # ----------
        self.background = Background(
            x_delta=self.screen_delta,
            window=self.window,
            screen_width=self.window_width,
            screen_height=self.window_height,
        )

        # ZAPPERS
        # -------
        self.zappers: List[Zapper] = []
        for index in range(self.window_width // self.zapper_spacing):
            _zapper = Zapper(
                window=self.window,
                screen_width=self.window_width,
                screen_height=self.window_height,
                x_delta=self.screen_delta,
                x_start_position=self.window_width + (self.zapper_spacing * index),
                y_position=random.randint(
                    self.lower_spawn_bound, self.upper_spawn_bound
                ),
                rotation=random.randint(ROTATE_LOWER, ROTATE_UPPER),
            )
            self.zappers.append(_zapper)

        # COINS
        # -----
        self.coins: List[Coin] = []
        for index in range(self.window_width // self.coin_spacing):
            _coin = Coin(
                window=self.window,
                screen_width=self.window_width,
                screen_height=self.window_height,
                x_delta=self.screen_delta,
                x_start_position=self.window_width + (self.coin_spacing * index) +( self.zapper_spacing // 2),
                y_position=random.randint(
                    self.lower_spawn_bound, self.upper_spawn_bound
                ),
            )
            self.coins.append(_coin)

        # PLAYERS
        # -------
        self.players: List[Player] = []
        for _ in range(len(self.ais)):
            _player = Player(
                window=self.window,
                screen_width=self.window_width,
                screen_height=self.window_height,
                y_delta=self.screen_delta,
            )
            self.players.append(_player)

    def play_game(self, length: int, generation: int, draw_vision: bool = False):
        """A function to play the game!

        Args:
            length (int): how many frames the game is to be played for
            generation (int): which generation the AIs are on
        """

        # for each frame in the frame
        for _ in range(length):
            # Allowing the user to click the x button and quit out of the game
            for game_event in event.get():
                if game_event.type == QUIT:
                    pygame_quit()
                    quit()

            # Checking if all of the AIs are dead, and if so, to exit the game
            if all([player.is_dead for player in self.players]):
                break

            # BACKGROUND
            # ----------
            self.background.update_frame()

            # GAME STATS
            # ----------
            # Max Points
            self.window.blit(
                self.stats_font.render(
                    f"Max Points: {max([ player.score for player in self.players]):4}",
                    1,
                    (255, 0, 0),
                ),
                (self.window_width - self.window_width // TEXT_X_RATIO, TEXT_BOARDER),
            )
            # Generation
            self.window.blit(
                self.stats_font.render(f"Generation: {generation}", 1, (255, 0, 0)),
                (
                    self.window_width - self.window_width // TEXT_X_RATIO,
                    TEXT_BOARDER + self.window_height // FONT_RATIO,
                ),
            )
            # Alive
            self.window.blit(
                self.stats_font.render(
                    f"Alive: {sum([1 for player in self.players if not player.is_dead])}/{len(self.players)}",
                    1,
                    (255, 0, 0),
                ),
                (
                    self.window_width - self.window_width // TEXT_X_RATIO,
                    TEXT_BOARDER + self.window_height // (FONT_RATIO / 2),
                ),
            )

            # ZAPPERS
            # -------
            # init values for the nearest zapper
            min_zapper_x = float("inf")
            top_y_zapper = -1
            bottom_y_zapper = -1
            zapper_index = -1
            # itterating over all of the zappers and moving them
            for index, zapper in enumerate(self.zappers):
                zapper.update_frame()
                # if the zapper is outside of the frame, to reset it's position
                if zapper.zapper_sprite.image.get_rect().right + zapper.x_position <= 0:
                    zapper.reset(
                        y_position=random.randint(
                            self.lower_spawn_bound, self.upper_spawn_bound
                        ),
                        rotation=random.randint(ROTATE_LOWER, ROTATE_UPPER),
                        x_position=self.window_width + zapper.x_position,
                    )
                # Checking if the zapper is the closest to the player, and if so updating the varibles
                if zapper.x_position < min_zapper_x:
                    # comparison values update
                    zapper_index = index
                    min_zapper_x = zapper.x_position
                    # getting image dimensions
                    zapper_image_rectangle = zapper.zapper_sprite.image.get_rect()
                    #player_imgage_rectangle = self.players[0].height // 2
                    # getting vertical bounds
                    # NOTE we are dividng by 2, because the y position is the center
                    top_y_zapper = zapper.y_position - zapper_image_rectangle.bottom // 2 #- player_imgage_rectangle
                    bottom_y_zapper = zapper.y_position + zapper_image_rectangle.bottom // 2 #+ player_imgage_rectangle
            # displaying what the AI sees
            if draw_vision:
                pygame.draw.line(
                    self.window,
                    (255, 0, 0),
                    (min_zapper_x, top_y_zapper),
                    (min_zapper_x, bottom_y_zapper),
                    AI_VISION_BOLD,
                )

            # COINS
            # -----
            # init values for the nearest coin
            min_coin_x = float("inf")
            center_y_coin = -1
            coin_index = -1
            # a value for if the coin was collected or not. If true, the coin resets
            reset_coin = False
            # itterating over all of the coins and moving them
            for index, coin in enumerate(self.coins):
                coin.update_frame()
                # if the coin is outside of the frame, to reset it's position
                if (coin.x_position + coin.width // 2) <= 0:
                    coin.reset(
                        y_position=random.randint(
                            self.lower_spawn_bound, self.upper_spawn_bound
                        ),
                        x_position=self.window_width,
                    )
                # Checking if coin zapper is the closest to the player, and if so updating the varibles
                if coin.x_position < min_coin_x:
                    # comparison values update
                    min_coin_x = coin.x_position
                    coin_index = index
                    # getting y position (center of coin)
                    center_y_coin = coin.y_position
            # displaying what the AI sees
            if draw_vision:
                pygame.draw.circle(
                    self.window,
                    (0, 255, 0),
                    (min_coin_x, center_y_coin),
                    AI_VISION_BOLD,
                )

            # PLAYERS
            # -------
            # itterating over all of the players and moving them accordingly
            for player, ai in zip(self.players, self.ais):
                # if the player is dead, they can not move or get points
                if player.is_dead:
                    continue

                # moving the player based on the forward propagation of the ai
                player.update_frame(
                    ai.forward_propagate(
                        player_y=player.y_position / self.window_height,
                        nearest_coin_y_center=center_y_coin / self.window_height,
                        zapper_y_bottom=bottom_y_zapper / self.window_height,
                        zapper_y_top=top_y_zapper / self.window_height,
                    )
                )

                # Checking to see if the player is touching a zapper, and if so, killing them!
                player.is_dead = sprite.collide_mask(
                    player.player_sprite, self.zappers[zapper_index].zapper_sprite
                )

                # giving the player a reward for being alive
                player.score += self.alive_reward

                # if the player is touching the closest coin
                if sprite.collide_mask(
                    player.player_sprite, self.coins[coin_index].coin_sprite
                ):
                    # increase the player score, and remember to remove the coin
                    player.score += self.coin_reward
                    reset_coin = True

            # if a player or more collided with a coin, then we want to reset the coin
            if reset_coin:
                self.coins[coin_index].reset(
                    y_position=random.randint(
                        self.lower_spawn_bound, self.upper_spawn_bound
                    ),
                    x_position=self.window_width + self.coins[coin_index].x_position,
                )

            # updating the game and sleeping per fps
            display.flip()
            self.clock.tick(self.fps)

        # rewarding the players who are alive
        for player in self.players:
            if not player.is_dead:
                player.score += self.complete_reward
