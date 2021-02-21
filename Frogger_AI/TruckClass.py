# Important Imports
import pygame
import random

import Utils

# A class for the trucks
class Truck:
    
    def __init__(self,y,side,x = 0):
        # Initializations
        self.y = y
        self.VEL = random.randrange(10,15)
        self.side = side
        self.name = 'truck'

        # Deciding weither the truck is a small or large one
        if random.randrange(2): self.img = Utils.TRUCK_LG_IMG
        else: self.img = Utils.TRUCK_SM_IMG
        
        # since the trucks approach at different sides, I have the side decision in the class not the game
        if side: self.x = -1 * self.img.get_width()
        else:
            self.x = Utils.WINDOW_WIDTH
            self.img = pygame.transform.flip(self.img,True,True)
            self.VEL *= -1
        # manual overide for x
        if x: self.x = x
   
    # A function to move the truck
    def move(self):
        self.x += self.VEL
    
    # A function to draw the truck
    def draw(self,window):
        window.blit(self.img,(self.x,self.y))
    
    # if the truck is off the screen return true to be removed from the list
    def off_screen(self):
        if self.side and self.x > Utils.WINDOW_WIDTH: return True
        if not self.side and self.x  < (-1 * self.img.get_width()): return True
        return False

    # getting the area covered by the truck sprite
    def get_mask(self):
        return pygame.mask.from_surface(self.img)