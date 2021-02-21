# Important Imports
import pygame
import os
# initializing the window
pygame.font.init()
WINDOW_WIDTH = 600
WINDOW_HIGHT = 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HIGHT))
pygame.display.set_caption("Frogger AI")
# init the font
STAT_FONT = pygame.font.SysFont("comicsans", 50)
# initalizing the pictures
FROG_IMG = pygame.image.load(os.path.join("images","FROG.png"))
SENSOR_SAFE_IMG = pygame.image.load(os.path.join("images","SENSOR-SAFE.png")).convert_alpha()
SENSOR_DANGER_IMG = pygame.image.load(os.path.join("images","SENSOR-DANGER.png")).convert_alpha()
TRUCK_LG_IMG = pygame.image.load(os.path.join("images","TRUCK-LG.png")).convert_alpha()
TRUCK_SM_IMG = pygame.image.load(os.path.join("images","TRUCK-SM.png")).convert_alpha()
LOG_LG_IMG = pygame.image.load(os.path.join("images","LOG-LG.png")).convert_alpha()
LOG_SM_IMG = pygame.image.load(os.path.join("images","LOG-SM.png")).convert_alpha()
BG_IMG = pygame.image.load(os.path.join("images","BG.png")).convert_alpha()
# some global values to be used
gen = 0
DRAW_LINES = False
# a funtion to show the GUI
def draw_window(frogs, trucks, logs, score):
    # draw the background
    WINDOW.blit(BG_IMG, (0,0))
    # draw the trucks
    for lane in trucks: 
        for truck in lane: 
            truck.draw(WINDOW)
    # draw the logs
    for lane in logs:
        for log in lane: 
            log.draw(WINDOW)
    # draw the frogs
    for frog in frogs:
        frog.draw(WINDOW)
    # reward
    score_label = STAT_FONT.render("Max Reward: " + str(round(13.5 + score,2)),1,(0,0,0))
    WINDOW.blit(score_label,(WINDOW_WIDTH - score_label.get_width() - 15, 10))
    # generations
    score_label = STAT_FONT.render("Gens: " + str(gen-1),1,(0,0,0))
    WINDOW.blit(score_label, (10, 10))
    # alive
    score_label = STAT_FONT.render("Alive: " + str(len(frogs)),1,(0,0,0))
    WINDOW.blit(score_label, (10, 50))
    # display the window
    pygame.display.update()