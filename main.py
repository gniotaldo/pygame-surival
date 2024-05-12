import pygame
import random
from typing import List
from pygame.math import Vector2
from pygame.locals import *
from misc.config import *
from misc.images import bottomBarImg
from classes.Map import Map
from classes.Agent import Agent
from classes.mapObjects.Rock import Rock
from classes.mapObjects.IronOre import IronOre
from classes.mapObjects.Lily import Lily
from classes.mapObjects.Tree import Tree
from classes.mapObjects.Water import Water


def displayBar():
    DISPLAY.blit(
        bottomBarImg,
        (0, HEIGHT*TILE_SIZE))
    inventory_counts = {}

    # Zliczenie elementów w ekwipunku agenta
    for item in agent.inventory:
        inventory_counts[item] = inventory_counts.get(item, 0) + 1

    # Pozycja startowa dla wypisywania na pasku
    x_pos = 10
    y_pos = HEIGHT * TILE_SIZE + 10

    # Wypisanie elementów na pasku
    for item, count in inventory_counts.items():
        text = font.render(f"{item}: {count}", True, (255, 255, 255))
        DISPLAY.blit(text, (x_pos, y_pos))
        x_pos += text.get_width() + 10  


def tick():
    CLOCK.tick(FRAMERATE)
    world_map.render(DISPLAY)
    for object in objects:
        object.render(DISPLAY)
    agent.render(DISPLAY)
    displayBar()
    pygame.display.flip()
    pygame.display.update()

    

if __name__ == '__main__': 
    pygame.init()
    font = pygame.font.SysFont(None, 25)
    world_map = Map(WIDTH, HEIGHT, TILE_SIZE)
    trees = [Tree(Vector2(x, y), TILE_SIZE, WIDTH, HEIGHT) for (x, y) in world_map.tree_cells]
    rocks = [Rock(Vector2(x, y), TILE_SIZE, WIDTH, HEIGHT) for (x, y) in world_map.rock_cells]
    waters = [Water(Vector2(x, y), TILE_SIZE, WIDTH, HEIGHT) for (x, y) in world_map.water_cells]
    lilies = [Lily(Vector2(x, y), TILE_SIZE, WIDTH, HEIGHT) for (x, y) in world_map.lily_cells]
    ironOres = [IronOre(Vector2(x, y), TILE_SIZE, WIDTH, HEIGHT) for (x, y) in world_map.ironOre_cells]
    objects = trees + rocks + waters + lilies + ironOres
    agent = Agent(TILE_SIZE,world_map)
    is_running = True
    paused = False
    ticks = 0
    print(world_map.map_grid[0][0])

    while is_running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif not paused:
                    if event.key == pygame.K_w:
                        agent.move('W',world_map)
                        rendLeft = agent.position.x - 15
                        rendTop = agent.position.y - 10
                    elif event.key == pygame.K_s:
                        agent.move('S',world_map)
                        rendLeft = agent.position.x - 15
                        rendTop = agent.position.y - 10
                    elif event.key == pygame.K_a:
                        agent.move('A',world_map)
                        rendLeft = agent.position.x - 15
                        rendTop = agent.position.y - 10
                    elif event.key == pygame.K_d:
                        agent.move('D',world_map)
                        rendLeft = agent.position.x - 15
                        rendTop = agent.position.y - 10
                    elif event.key == pygame.K_q:
                        if world_map.map_grid[int(agent.facing.x)][int(agent.facing.y)] == Map.Cell.LilyCell:
                            objects.append(Water(agent.facing,TILE_SIZE,WIDTH,HEIGHT))
                        agent.destroy(objects)

        if paused: 
            continue
        tick()
        ticks += 1
    pygame.quit()
