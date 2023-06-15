from pygame import image, Surface, transform

BACKGROUND_FILE = "images/background.jpg"

class Background:
    def __init__(
        self, x_delta: int, window: Surface, screen_width: int, screen_height: int
    ):
        """a class for the background (moving). We move the background across the x axis to give the illusion that the player is running

        Args:
            x_delta (int): the speed at which the background moves
            window (Surface): the main window that the background is attached to
            screen_width (int): how wide the screen is
            screen_height (int): how tall the screen is
        """
        # defaults
        self.x_position = 0

        # taking the inputs and setting the varibles
        self.window = window
        self.x_delta = x_delta
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Creating an image for the backgound
        self.background_image = transform.scale(
            image.load(BACKGROUND_FILE), (self.screen_width, self.screen_height)
        )

    def move(self):
        """A function to move the background along the x axis
        """
        # moves the background x frames to the left
        self.x_position -= self.x_delta

        # if the background is off screen, we reset the x position
        if self.x_position < -self.screen_width:
            self.x_position = 0

    def draw(self):
        """A function to draw the background on the screen
        """
        # Drawling the left image
        self.window.blit(self.background_image, (self.x_position, 0))
        # Drawling the right image
        self.window.blit(
            self.background_image, (self.x_position + self.screen_width, 0)
        )

    def update_frame(self):
        """A function to abstract the move and draw
        """
        self.move()
        self.draw()
