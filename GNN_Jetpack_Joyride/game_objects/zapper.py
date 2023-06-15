from pygame import image, Surface, transform, sprite, mask

ZAPPER_FILE = "images/zap.png"
ZAPPER2_FILE = "images/zap2.png"

WIDTH_RATIO = 6
HEIGHT_RATIO = 10
ANIMATION_LENGTH = 10


class Zapper:
    def __init__(
        self,
        x_delta: int,
        x_start_position: int,
        y_position: int,
        window: Surface,
        screen_width: int,
        screen_height: int,
        rotation: int,
    ):
        """A class for the zapper object to move along the x axis

        Args:
            x_delta (int): the speed at which the zapper moves across the x-axis
            x_start_position (int): the starting x position of the sprite
            y_position (int): where along the y axis to travel
            window (Surface): the main window that the background is attached to
            screen_width (int): how wide the screen is
            screen_height (int): how tall the screen is
            rotation (int): which way to rotate the sprite
        """
        # taking the inputs and setting the varibles
        self.x_delta = x_delta
        self.x_position = x_start_position
        self.y_position = y_position
        self.window = window
        self.width = screen_width // WIDTH_RATIO
        self.height = screen_height // HEIGHT_RATIO
        self.rotation = rotation

        # Sprite varibles
        # getting the images
        self.unmodified_zapper_image_1 = transform.scale(
            image.load(ZAPPER_FILE), (self.width, self.height)
        )
        self.unmodified_zapper_image_2 = transform.scale(
            image.load(ZAPPER2_FILE), (self.width, self.height)
        )
        # rotating the images
        self.zapper_image_1 = transform.rotate(
            self.unmodified_zapper_image_1, self.rotation
        )
        self.zapper_image_2 = transform.rotate(
            self.unmodified_zapper_image_2, self.rotation
        )
        # setting the animation
        self.animation_counter = 0
        self.animation_length = ANIMATION_LENGTH
        # creating the sprite
        self.zapper_sprite = sprite.Sprite()
        self.zapper_sprite.image = self.zapper_image_1
        self.zapper_sprite.rect = self.zapper_sprite.image.get_rect(
            center=(self.x_position, self.y_position)
        )
        self.zapper_sprite.mask = mask.from_surface(self.zapper_sprite.image)

    def move(self):
        """A function to move the zapper along the x axis
        """
        # moving the x position to the left
        self.x_position -= self.x_delta

        # animation updates
        # increasing the counter by 1. This is so the image doesn't flash at 1/FPS
        self.animation_counter += 1
        # if the animation counter is longer than the allowed length, we will toggle the sprite and reset the counter
        if self.animation_counter > self.animation_length:
            self.animation_counter = 0
            self.zapper_sprite.image = (
                self.zapper_image_2
                if self.zapper_sprite.image == self.zapper_image_1
                else self.zapper_image_1
            )
        # Updating our sprite with the new image location + mask
        self.zapper_sprite.rect = self.zapper_sprite.image.get_rect(
            center=(self.x_position, self.y_position)
        )
        self.zapper_sprite.mask = mask.from_surface(self.zapper_sprite.image)

    def draw(self):
        """A function to draw the sprite on the window
        """
        self.window.blit(self.zapper_sprite.image, self.zapper_sprite.rect)

    def update_frame(self):
        """A function to abstract the move and draw
        """
        self.move()
        self.draw()

    def reset(self, y_position: int, rotation: int, x_position: int):
        """A function to reset the x and y position as well as adjust the rotation of the sprite

        Args:
            y_position (int): the new y position
            rotation (int): the new rotation
            x_position (_type_): the new x position
        """
        # updating the location + rotation
        self.y_position = y_position
        self.rotation = rotation
        self.x_position = x_position

        # updating the sprite
        self.zapper_image_1 = transform.rotate(
            self.unmodified_zapper_image_1, self.rotation
        )
        self.zapper_image_2 = transform.rotate(
            self.unmodified_zapper_image_2, self.rotation
        )
        self.zapper_sprite.image = self.zapper_image_1
        self.zapper_sprite.rect = self.zapper_sprite.image.get_rect(
            center=(self.x_position, self.y_position)
        )
        self.zapper_sprite.mask = mask.from_surface(self.zapper_sprite.image)
