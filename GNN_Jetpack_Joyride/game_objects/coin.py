from pygame import image, Surface, transform, sprite, mask

COIN_FILE = "images/coin.png"
COIN2_FILE = "images/coin2.png"

WIDTH_RATIO = 20
HEIGHT_RATIO = 20
ANIMATION_LENGTH = 10

class Coin:
    def __init__(
        self,
        x_delta: int,
        x_start_position: int,
        y_position: int,
        window: Surface,
        screen_width: int,
        screen_height: int,
    ):
        """A class for the coin objects in the game

        Args:
            x_delta (int): the change in how fast along the x axis the coin will travel
            x_start_position (int): where along the x axis to start
            y_position (int): where along the y axis to travel
            window (Surface): the main window that the background is attached to
            screen_width (int): how wide the screen is
            screen_height (int): how tall the screen is
        """
        # taking the inputs and setting the varibles
        self.x_position = x_start_position
        self.window = window
        self.x_delta = x_delta
        self.y_position = y_position

        # Sprite varibles
        self.animation_counter = 0
        self.animation_length = ANIMATION_LENGTH
        self.width = screen_width // WIDTH_RATIO
        self.height = screen_height // HEIGHT_RATIO

        # images
        self.coin_image_1 = transform.scale(
            image.load(COIN_FILE), (self.width, self.width)
        )
        self.coin_image_2 = transform.scale(
            image.load(COIN2_FILE), (self.width, self.width)
        )

        # sprite
        self.coin_sprite = sprite.Sprite()
        self.coin_sprite.image = self.coin_image_1
        self.coin_sprite.rect = self.coin_sprite.image.get_rect(
            center=(self.x_position, self.y_position)
        )
        self.coin_sprite.mask = mask.from_surface(self.coin_sprite.image)

    def move(self):
        """A function to move the coin across the x axis + update the sprite
        """
        # moving the x position to the left
        self.x_position -= self.x_delta

        # animation updates
        # increasing the counter by 1. This is so the image doesn't flash at 1/FPS
        self.animation_counter += 1
        # if the animation counter is longer than the allowed length, we will toggle the sprite and reset the counter
        if self.animation_counter > self.animation_length:
            self.animation_counter = 0
            self.coin_sprite.image = (
                self.coin_image_2
                if self.coin_sprite.image == self.coin_image_1
                else self.coin_image_1
            )
        # Updating our sprite with the new image location + mask
        self.coin_sprite.rect = self.coin_sprite.image.get_rect(
            center=(self.x_position, self.y_position)
        )
        self.coin_sprite.mask = mask.from_surface(self.coin_sprite.image)

    def draw(self):
        """A function to draw the sprite on the window
        """
        self.window.blit(self.coin_sprite.image, self.coin_sprite.rect)

    def update_frame(self):
        """A function to abstract the move and draw
        """
        self.move()
        self.draw()

    def reset(self, y_position: int, x_position):
        """A function to reset the coin's x and y position

        Args:
            y_position (int): the new y position
            x_position (_type_): the new x position
        """
        # updating the coins position
        self.y_position = y_position
        self.x_position = x_position

        # updating the sprites position
        self.coin_sprite.rect = self.coin_sprite.image.get_rect(
            center=(self.x_position, self.y_position)
        )
        self.coin_sprite.mask = mask.from_surface(self.coin_sprite.image)
