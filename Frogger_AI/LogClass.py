# Important Imports
import pygame
import random

import Utils

# A class for the logs
class Log:
    
    def __init__(self,y,side,x = 0):
        # Initializations
        self.y = y
        self.VEL = random.randrange(10,15)
        self.side = side
        self.name = 'log'

        # Deciding weither the log is a small or large one
        if random.randrange(2): self.img = Utils.LOG_LG_IMG
        else: self.img = Utils.LOG_SM_IMG

        # since the logs approach at different sides, I have the side decision in the class not the game
        if side: self.x = -1 * self.img.get_width()
        else:
            self.x = Utils.WINDOW_WIDTH
            self.VEL *= -1
        # manual overide for x
        if x: self.x = x
        
    # A function to move the log
    def move(self):
        self.x += self.VEL
    
    # A function to draw the log
    def draw(self,window):
        window.blit(self.img,(self.x,self.y))
    
    # if the log is off the screen return true to be removed from the list
    def off_screen(self):
        if self.side and self.x > Utils.WINDOW_WIDTH: return True
        if not self.side and self.x  < (-1 * self.img.get_width()): return True
        return False

    # getting the area covered by the log sprite
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

        
