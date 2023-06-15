from pygame import image, Surface, transform, sprite, mask

PLAYER_RUNNING_1_FILE = "images/run1.png"
PLAYER_RUNNING_2_FILE = "images/run2.png"
PLAYER_FLYING_FILE = "images/fly.png"

WIDTH_RATIO = 10
HEIGHT_RATIO = 10
ANIMATION_LENGTH = 10
UPPER_BOUNDS_RATIO = 1.5
LOWER_BOUNDS_RATIO = 2


class Player:
    def __init__(
        self, y_delta: int, window: Surface, screen_width: int, screen_height: int
    ):
        """a class for the player object to move along the y axis

        Args:
            y_delta (int): the change in speed along the y axis
            window (Surface): the main window that the background is attached to
            screen_width (int): how wide the screen is
            screen_height (int): how tall the screen is
        """
        # taking the inputs and setting the varibles
        self.window = window
        self.y_delta = y_delta
        self.screen_height = screen_height

        # default gameplay varibles
        self.score = 0
        self.is_dead = False

        # sprite work
        # getting the dimensions
        self.width = screen_width // WIDTH_RATIO
        self.height = screen_height // HEIGHT_RATIO
        # players init position
        self.x_position = self.width // 2
        self.floor_y_position = screen_height - (self.height * LOWER_BOUNDS_RATIO)
        self.ciel_y_position = self.height * UPPER_BOUNDS_RATIO
        self.y_position = screen_height - (self.height * LOWER_BOUNDS_RATIO)
        # loading the images
        self.run1_image = transform.scale(
            image.load(PLAYER_RUNNING_1_FILE), (self.width, self.width)
        )
        self.run2_image = transform.scale(
            image.load(PLAYER_RUNNING_2_FILE), (self.width, self.width)
        )
        self.fly_image = transform.scale(
            image.load(PLAYER_FLYING_FILE), (self.width, self.width)
        )
        # animation changing varibles
        self.run_animation_toggle = True
        self.run_animation_counter = 0
        self.run_animation_length = ANIMATION_LENGTH
        # setting the image to run, because we know all sprites start on the floor
        self.active_image = self.run1_image
        # creating the sprite
        self.player_sprite = sprite.Sprite()
        self.player_sprite.image = self.run1_image
        self.player_sprite.rect = self.player_sprite.image.get_rect(
            center=(self.x_position, self.y_position)
        )
        self.player_sprite.mask = mask.from_surface(self.player_sprite.image)

    def move(self, is_flying: bool):
        """A function to move the player along the y axis

        Args:
            is_flying (bool): if True, then the player moves up, if false, then down
        """
        # moving the player up the y axis
        if is_flying:
            # you might be wondering why we are -= the position,
            # and it is because the pygame window has a point of reference at the top left
            self.y_position -= self.y_delta
            # if we hit the cieling, we set our position back to the cieling
            if self.y_position < (self.ciel_y_position):
                self.y_position = self.ciel_y_position
            # if we are flying, want want to make sure to update our sprite correctly
            self.player_sprite.image = self.fly_image
            self.player_sprite.rect = self.player_sprite.image.get_rect(
                center=(self.x_position, self.y_position)
            )
            self.player_sprite.mask = mask.from_surface(self.player_sprite.image)
            return

        # if we are not flying then we are falling, and will move down the y axis
        # you might be wondering why we are += the position,
        # and it is because the pygame window has a point of reference at the top left
        self.y_position += self.y_delta
        # if the player is below the floor we set them back at the floor
        if self.y_position > (self.floor_y_position):
            self.y_position = self.floor_y_position

            # if the player is on the ground, then we can continue the ground animation
            self.run_animation_counter += 1

            # toggling the players running sprite if it passes the target length
            if self.run_animation_counter > self.run_animation_length:
                self.run_animation_toggle = not self.run_animation_toggle
                self.run_animation_counter = 0

                self.player_sprite.image = (
                    self.run2_image
                    if self.player_sprite.image == self.run1_image
                    else self.run1_image
                )

        # updating the sprites location
        self.player_sprite.rect = self.player_sprite.image.get_rect(
            center=(self.x_position, self.y_position)
        )
        self.player_sprite.mask = mask.from_surface(self.player_sprite.image)

    def draw(self):
        """A function to draw the sprite on the window"""
        self.window.blit(self.player_sprite.image, self.player_sprite.rect)

    def update_frame(self, is_flying: float):
        """A function to abstract move and draw

        Args:
            is_flying (float): the AI input for if it is to fly or not.
                RANGE: -1 -> 1
        """
        self.move(is_flying=(is_flying >= 0))
        self.draw()
