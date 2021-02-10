# important imports
import pygame

import Utils

# a class for the ground
class Base:
    # moving the ground at the same rate that the cactus moves
    VEL = 15
    WIDTH = Utils.BASE_IMG.get_width()
    IMG = Utils.BASE_IMG

    def __init__(self):
        self.y = Utils.FLOOR - self.IMG.get_height()
        # making 2 grounds that way it looks continous 
        self.x1 = 0
        self.x2 = self.WIDTH
    
    # moving both grounds
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        # if the ground is off the screen, reset the ground
        if self.x1 + self.WIDTH < 0: self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0: self.x2 = self.x1 + self.WIDTH
    
    # a function to draw the ground
    def draw(self, window):
        window.blit(self.IMG,(self.x1,self.y))
        window.blit(self.IMG,(self.x2,self.y))
