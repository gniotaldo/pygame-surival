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

    for item in agent.inventory:
        inventory_counts[item] = inventory_counts.get(item, 0) + 1

    x_pos = 10
    y_pos = (HEIGHT+BOTTOMBAR/2) * TILE_SIZE - 5

    for item, count in inventory_counts.items():
        text = font.render(f"{item}: {count}", True, (255, 255, 255))
        DISPLAY.blit(text, (x_pos, y_pos))
        x_pos += text.get_width() + 10  

    texthelper = font.render("COORDS: 444.44, 444.44", True, (255, 255, 255))
    maxwidth = texthelper.get_width()
    textCords = font.render(f"COORDS: {agent.position.x}, {agent.position.y}", True, (255, 255, 255))
    DISPLAY.blit(textCords, (WIDTH * TILE_SIZE - maxwidth - 10, y_pos))


def tick():
    CLOCK.tick(FRAMERATE)
    world_map.render(DISPLAY, renderLeft, renderTop)
    for object in objects:
        if renderLeft-2 <= object.position.x < renderLeft +2 +WIDTH and renderTop-2 <= object.position.y < renderTop +2 + HEIGHT:
            object.render(DISPLAY, renderLeft, renderTop)
    agent.render(DISPLAY, renderLeft, renderTop)
    displayBar()
    pygame.display.flip()
    pygame.display.update()

def updateCamera():
    rendLeft = agent.position.x - WIDTH/2
    rendTop = agent.position.y - HEIGHT/2
    if rendTop < 0:
        rendTop = 0
    if rendTop > 9 * HEIGHT:
        rendTop = 9 * HEIGHT
    if rendLeft < 0:
        rendLeft = 0
    if rendLeft > 9 * WIDTH:
        rendLeft= 9 * WIDTH
    return rendLeft, rendTop

    

if __name__ == '__main__': 
    pygame.init()
    font = pygame.font.SysFont(None, 25)
    world_map = Map(WIDTH*MAP_SIZE, HEIGHT*MAP_SIZE, TILE_SIZE)
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
        renderLeft, renderTop = updateCamera()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif not paused:
                    '''
                    if event.key == pygame.K_w:
                        agent.move('W',world_map)
                    elif event.key == pygame.K_s:
                        agent.move('S',world_map)
                    elif event.key == pygame.K_a:
                        agent.move('A',world_map)
                        print(f"rendery: {renderLeft, renderTop}")
                    elif event.key == pygame.K_d:
                        agent.move('D',world_map)
                    '''
                    if event.key == pygame.K_q:
                        deleted, position = agent.destroy(objects)
                        if deleted == Map.Cell.LilyCell:
                            objects.append(Water(position,TILE_SIZE,WIDTH,HEIGHT))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            agent.move('W', world_map)
        if keys[pygame.K_s]:
            agent.move('S', world_map)
        if keys[pygame.K_a]:
            agent.move('A', world_map)
        if keys[pygame.K_d]:
            agent.move('D', world_map)


        if paused: 
            continue
        tick()
        ticks += 1
    pygame.quit()
