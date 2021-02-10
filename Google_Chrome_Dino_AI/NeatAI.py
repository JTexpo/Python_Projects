# important imports
import pygame
import random
import os
import time 
import neat
import visualize

import Utils
import DinoClass
import BaseClass
import CactusClass
import BirdClass

# A function to test thee AI
def eval_genomes(genomes, config):
    # incrementing gen
    Utils.gen += 1
    # AI inits
    nets = []
    dinos = []
    ge = []
    # creating nn's and adding them into an array of nets
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        dinos.append(DinoClass.Dino(150,Utils.FLOOR-Utils.DINO_IMGS_RUN[0].get_height()))
        ge.append(genome)
    # Game inits
    base = BaseClass.Base()
    # Deciding the first obstical
    if random.randrange(2): obsticals = [CactusClass.Cactus(Utils.WINDOW_WIDTH)]
    else: obsticals = [BirdClass.Bird(Utils.WINDOW_WIDTH,Utils.BIRD_RANGE[random.randrange(3)])]
    score = 0
    clock = pygame.time.Clock()
    run = True
    # game loop
    while run and len(dinos) > 0:
        # FPS
        clock.tick(30)
        # if the user closes the tab
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break
        # varibles that show 
        obsticals_index = 0
        # determining which bird / cactus to reference
        if len(dinos) > 0:
            if len(obsticals) > 1 and dinos[0].x > obsticals[0].x + obsticals[0].img.get_width(): obsticals_index = 1
        # itterating through all the dinos and getting their decision
        for x, dino in enumerate(dinos):
            dino.move()
            # NN forward prop
            output = nets[x].activate((
                    # distance from obstical to dino
                    abs(dino.x - obsticals[obsticals_index].x),
                    # distance from obstical to floor
                    Utils.FLOOR - obsticals[obsticals_index].y - obsticals[obsticals_index].img.get_height() - 65
                ))
            # Finding the most desirable move
            if output[0] > output[1] and output[0] > .5: dino.jump()
            elif output[1] > .5: dino.duck()
        # moving the ground
        base.move()
        # checking if the dino past the obstical
        for obst in obsticals:
            # move the obsticals
            obst.move()
            for dino in dinos:
                # check collisions, and if collision then remove dino
                if obst.collide(dino,Utils.WINDOW):
                    ge[dinos.index(dino)].fitness -= 1
                    nets.pop(dinos.index(dino))
                    ge.pop(dinos.index(dino))
                    dinos.pop(dinos.index(dino))
            # if the obstical is off of the map remove the obstical
            if obst.x + obst.img.get_width() < 0: obsticals.remove(obst) 
            # if the object is passed add another object
            if not obst.passed and obst.x < dino.x:
                obst.passed = True
                score += 1
                for genome in ge: genome.fitness += 1
                if random.randrange(2): obsticals.append(CactusClass.Cactus(Utils.WINDOW_WIDTH))
                else: obsticals.append(BirdClass.Bird(Utils.WINDOW_WIDTH,Utils.BIRD_RANGE[random.randrange(3)]))            
        # Drawling the game
        Utils.draw_window(
            Utils.WINDOW,
            dinos,
            obsticals,
            base,
            score,
            Utils.gen,
            obsticals_index,
        )
        # end condition
        if score == 100: return
        
# A function to create and report about the AI
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
            