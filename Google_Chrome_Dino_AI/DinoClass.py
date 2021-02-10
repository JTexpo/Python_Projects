# important imports
import pygame

import Utils

# A class for the dino (player) in the game
class Dino:
    # Because the dino does not 
    RUN_IMGS = Utils.DINO_IMGS_RUN
    JUMP_IMG = Utils.DINO_IMG_JUMP
    DUCK_IMGS = Utils.DINO_IMGS_DUCK
    ANIMATION_TIME = 5
    VEL = -10.5

    def __init__(self,x,y):
        # placement 
        self.x = x
        self.y = y
        self.height = self.y
        # move varibles
        self.tick_count = 0
        self.has_jump = False
        self.has_duck = False
        # graphic varibles 
        self.img_count = 0
        self.img_ID = 0
        self.img = self.RUN_IMGS[0]

    # a function that moves that unlocks the ability to jump
    def jump(self):
        # no double jumping allowed
        if not self.has_jump:
            self.has_jump = True
            self.has_duck = False
            self.tick_count = 0
            self.height = self.y
    
    # a function to duck, this overides jump
    def duck(self):
        self.y = Utils.FLOOR - self.RUN_IMGS[0].get_height()
        self.has_jump = False
        self.has_duck = True
        self.tick_count = 0

    # the main move function
    def move(self):
        # Jump condition
        if self.has_jump:
            # slowly incrementin the tick timer
            self.tick_count += .5
            # PHYSICS
            # d = v * t + .5 * a * t ^ 2
            displacement = self.VEL*(self.tick_count) + .5*(3)*(self.tick_count)**2
            # if there is no room to fall, exit out of fall and set height to defualt, else jump/fall 
            if self.y + displacement >= Utils.FLOOR - self.RUN_IMGS[0].get_height():
                self.y = Utils.FLOOR - self.RUN_IMGS[0].get_height()
                self.has_jump = False
            else: self.y += displacement
        # duck condition, ducked for 1 frame
        if self.has_duck:
            if self.tick_count: self.has_duck = False
            self.tick_count += 1

    # a function to draw
    def draw(self,window):
        # changing to jump sprite
        if self.has_jump: self.img = self.JUMP_IMG
        # changing to duck sprite
        elif self.has_duck:
            self.img_count += 1
            if self.img_count > self.ANIMATION_TIME:
                self.img_ID = int(not(bool(self.img_ID)))
                self.img = self.DUCK_IMGS[self.img_ID]
                self.img_count = 0
        # changing to run sprite
        else:
            self.img_count += 1
            if self.img_count > self.ANIMATION_TIME:
                self.img_ID = int(not(bool(self.img_ID)))
                self.img = self.RUN_IMGS[self.img_ID]
                self.img_count = 0
        # window draw
        window.blit(self.img, (self.x,self.y))
    
    # getting the pygames mask
    def get_mask(self):
        return pygame.mask.from_surface(self.img)