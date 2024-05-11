import pygame
import random
from typing import List
from pygame.math import Vector2
from pygame.locals import *
from misc.config import *
from misc.images import barImg
from classes.Map import Map
from classes.Agent import Agent
from classes.Table import Tree
from classes.Meal import spaghetti, pizza, burger, menu
from misc.dictionary import names, surnames

def tick():
    CLOCK.tick(FRAMERATE)
    world_map.render(DISPLAY)
    for tree in trees:
        tree.render(DISPLAY)
    agent.render(DISPLAY)
    pygame.display.flip()
    pygame.display.update()
    

if __name__ == '__main__': 
    pygame.init()
    font = pygame.font.SysFont(None, 25)
    world_map = Map(WIDTH, HEIGHT, TILE_SIZE)
    agent = Agent(TILE_SIZE,world_map)
    world_map.set_map()
    trees = [Tree(Vector2(x, y), TILE_SIZE, WIDTH, HEIGHT) for (x, y) in world_map.tree_cells]
    is_running = True
    paused = False
    ticks = 0

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                else:
                    if event.key == pygame.K_w:
                        agent.move('W',world_map)
                    elif event.key == pygame.K_s:
                        agent.move('S',world_map)
                    elif event.key == pygame.K_a:
                        agent.move('A',world_map)
                    elif event.key == pygame.K_d:
                        agent.move('D',world_map)


        if paused: continue
       
        tick()
        ticks += 1
    pygame.quit()
