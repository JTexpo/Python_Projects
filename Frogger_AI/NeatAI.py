# Important imports
import pygame
import random
import os
import time
import neat 
import visualize

import Utils
import LogClass
import FrogClass
import TruckClass

# A function to run the games / evaluate the AI
def eval_genomes(genomes, config):
    # Initilizations
    Utils.gen += 1
    nets = []
    frogs = []
    ge = []
    fit = 10
    # creating all of the DNN's and their Frogs & Genomes
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        frogs.append(FrogClass.Frog(Utils.WINDOW_WIDTH/2,Utils.WINDOW_HIGHT,Utils.DRAW_LINES))
        ge.append(genome)

    # Initializing the Trucks and logs so the AI can spam going forward
    trucks = [[TruckClass.Truck(360,0,Utils.WINDOW_WIDTH/2+100)],
            [TruckClass.Truck(400,1,Utils.WINDOW_WIDTH/2-100)],
            [TruckClass.Truck(440,0,Utils.WINDOW_WIDTH/2+100)],
            [TruckClass.Truck(480,1,Utils.WINDOW_WIDTH/2-100)]]
    logs = [[LogClass.Log(120,0,Utils.WINDOW_WIDTH/2+100)],
            [LogClass.Log(160,1,Utils.WINDOW_WIDTH/2-100)],
            [LogClass.Log(200,0,Utils.WINDOW_WIDTH/2+100)],
            [LogClass.Log(240,1,Utils.WINDOW_WIDTH/2-100)],
            [LogClass.Log(280,0,Utils.WINDOW_WIDTH/2+100)]]
    while fit > 0:
        # FPS
        clock = pygame.time.Clock()
        clock.tick(30)
        fit -= .1
        # if the user closes the tab
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break
        
        '''
        MOVE FROGS
        ----------
        '''
        for x, frog in enumerate(frogs):
            output = nets[x].activate((
                frog.rsv,
                frog.lsv,
                frog.tsv
            ))
            # Moving Left
            if output[0] > .5 and output[0] > output[1] and output[0] > output[2]: frog.move(1)
            # Moving Right
            elif output[1] > .5 and output[1] > output[2]: frog.move(2)
            # Moving Up
            elif output[2] > .5: frog.move(3)
            # actually moving the frog
            frog.update()

        '''
        TRUCKS
        ------
        '''
        for side, lane in enumerate(trucks):
            # if the lane is empty add a truck
            if not len(lane): lane.append(TruckClass.Truck(360+40*side,side%2))
            # move all the trucks in a lane
            for truck in lane:
                truck.move()
                # Check Frog colission
                for frog in frogs: frog.colission(truck)
                # if the truck half way on the screen
                if (len(lane) < 2 and (
                    (truck.x > Utils.WINDOW_WIDTH / 2 and truck.side) or
                    (truck.x < Utils.WINDOW_WIDTH / 2 and not truck.side))):
                    lane.append(TruckClass.Truck(360+40*side,side%2))
                # if the truck is off screen remove it
                if truck.off_screen(): lane.remove(truck)
        
        '''
        LOGS
        ----
        '''
        for side, lane in enumerate(logs):
            # if the lane is empty add a log
            if not len(lane): lane.append(LogClass.Log(120+40*side,side%2))
            # move all the logs in a lane
            for log in lane:
                log.move()
                # Check Frog colission
                for frog in frogs: frog.colission(log)
                # if the log half way on the screen
                if (len(lane) < 2 and (
                    (log.x > Utils.WINDOW_WIDTH / 2 and log.side) or
                    (log.x < Utils.WINDOW_WIDTH / 2 and not log.side))):
                    lane.append(LogClass.Log(120+40*side,side%2))
                # if the log is off screen remove it
                if log.off_screen(): lane.remove(log)
        
        '''
        FROG UPDATE / FITNESS
        ---------------------
        '''
        for frog in frogs:
            if frog.game_over: 
                # The frog gets as far as it went
                ge[frogs.index(frog)].fitness = abs(Utils.WINDOW_HIGHT - frog.y) / 40
                # if the frog got to the end, add the time as a bonus
                if frog.y < 120: ge[frogs.index(frog)].fitness += fit
                # Removing the frog from the pool of frogs
                nets.pop(frogs.index(frog))
                ge.pop(frogs.index(frog))
                frogs.pop(frogs.index(frog))
        # if the time has run out than set all frogs states to game over
        if fit <= 0:
            for frog in frogs:
                ge[frogs.index(frog)].fitness = abs(Utils.WINDOW_HIGHT - frog.y) / 40
                nets.pop(frogs.index(frog))
                ge.pop(frogs.index(frog))
                frogs.pop(frogs.index(frog))
        # drawling the window
        Utils.draw_window(frogs, trucks, logs, fit)

def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))