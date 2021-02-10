# Important imports
import pygame
import random

import Utils

# The Cactus that is found in the game
class Cactus:
    # Speed at which the cactus scrolls across the screen
    VEL = 15

    def __init__(self,x):
        # Deciding weither it's a large or small cactus
        if random.randrange(2): 
            self.size = 'lg'
            self.img = Utils.LG_CACTUS_IMGS
        else:
            self.size = 'sm'
            self.img = Utils.SM_CACTUS_IMGS
        # Setting the x value from input, and y from img size
        self.x = x
        self.y = Utils.FLOOR - self.img.get_height() 
        self.passed = False
    
    # A function to scroll the cactus to the left
    def move(self):
        self.x -= self.VEL

    # A functino to display the cactus
    def draw(self,window):
        window.blit(self.img,(self.x,self.y))
    
    # a function to test if the dino has collided
    def collide(self,dino,window):
        dino_mask = dino.get_mask()
        cactus_mask = pygame.mask.from_surface(self.img)
        # getting the offset from the images sizes
        offest = (self.x - dino.x, self.y - round(dino.y))
        # if the two images overlap return true else false
        if dino_mask.overlap(cactus_mask,offest): return True
        return False
        