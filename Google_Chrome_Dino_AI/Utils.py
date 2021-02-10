# important imports
import pygame
import random
import os

'''
PYGAMES INITS
-------------
'''
# initalizing the font
pygame.font.init()  # init font
# Window Inits
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 300
FLOOR = 270
WINDOW = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Chrome Dino")
# Font Inits
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)
# Show what the AI sees, feel free to set this to False
DRAW_LINES = False
# IMAGE INITS
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("images","Bird" + str(x) + ".png"))) for x in range(2)]
DINO_IMGS_RUN = [pygame.transform.scale2x(pygame.image.load(os.path.join("images","DinoRun" + str(x) + ".png"))) for x in range(2)]
DINO_IMG_JUMP = pygame.transform.scale2x(pygame.image.load(os.path.join("images","DinoJump.png")))
DINO_IMGS_DUCK = [pygame.transform.scale2x(pygame.image.load(os.path.join("images","DinoDuck" + str(x) + ".png"))) for x in range(2)]
LG_CACTUS_IMGS = pygame.transform.scale2x(pygame.image.load(os.path.join("images","lgCactus0.png")).convert_alpha())
SM_CACTUS_IMGS = pygame.transform.scale2x(pygame.image.load(os.path.join("images","smCactus0.png")).convert_alpha())
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images","Base.png")).convert_alpha())
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images","BG.png")).convert_alpha())

# Gen Counter for visuals
gen = 0

# Option For Bird Spawns
BIRD_RANGE = [FLOOR, FLOOR - 65, FLOOR - 150]

# A function to display the backeng code, 
def draw_window(window, dinos, obsticals, base, score, gen, obsticals_index):
    # background
    window.blit(BG_IMG, (0,0))
    # base
    base.draw(window)
    # cactus
    for obst in obsticals: obst.draw(window)
    # Drawling the lines with the dino
    for dino in dinos:
        if DRAW_LINES:
            try:
                pygame.draw.line(
                    window,
                    (255,0,0),
                    (
                        dino.x+dino.img.get_width()/2, 
                        dino.y + dino.img.get_height()/2
                    ), 
                    (   
                        obsticals[obsticals_index].x + obsticals[obsticals_index].img.get_width()/2, 
                        obsticals[obsticals_index].y + obsticals[obsticals_index].img.get_height()/2
                    ), 
                    5
                )
            except Exception as err:
                pass
        dino.draw(window)
    # score
    score_label = STAT_FONT.render("Score: " + str(score),1,(0,0,0))
    window.blit(score_label,(WINDOW_WIDTH - score_label.get_width() - 15, 10))
    # generations
    score_label = STAT_FONT.render("Gens: " + str(gen-1),1,(0,0,0))
    window.blit(score_label, (10, 10))
    # alive
    score_label = STAT_FONT.render("Alive: " + str(len(dinos)),1,(0,0,0))
    window.blit(score_label, (10, 50))
    # show window
    pygame.display.update()
    