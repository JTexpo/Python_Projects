# important imports
import pygame

import Utils

# A class for the birds in the game
class Bird:
    # speed of the bird moving left
    VEL = 20
    # how many frames before the bird changes sprites
    ANIMATION_TIME = 5
    # bird sprites
    IMGS = Utils.BIRD_IMGS

    def __init__(self,x,y):
        self.img = self.IMGS[0]
        self.x = x
        self.y = y - self.img.get_height() 
        self.passed = False
        self.img_count = 0
        self.img_ID = 0
        
    # a function to move the bird to the left
    def move(self):
        self.x -= self.VEL

    # a function to draw the bird
    def draw(self,window):
        # image counter to decide when to flipt the image
        self.img_count += 1
        if self.img_count > self.ANIMATION_TIME:
            self.img_ID = int(not(bool(self.img_ID)))
            self.img = self.IMGS[self.img_ID]
            self.img_count = 0

        window.blit(self.img,(self.x,self.y))
    
    # a function to check if the dino sprite is overtop of a bird
    def collide(self,dino,window):
        dino_mask = dino.get_mask()
        bird_mask = pygame.mask.from_surface(self.img)
        # getting the offset from the images sizes
        offest = (self.x - dino.x, self.y - round(dino.y))
        # if the two images overlap return true else false
        if dino_mask.overlap(bird_mask,offest): return True
        return False
        