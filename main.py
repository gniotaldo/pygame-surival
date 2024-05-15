import pygame
import random
from typing import List
from pygame.math import Vector2
from pygame.locals import *
from misc.config import *
from misc.images import bottomBarImg, pausedImg, pausedIcon
from classes.Map import Map
from classes.Agent import Agent
import math

def displayBar():
    global inventory_counts, equipped_item_index, equipped_item, equipped_islast
    

    inventory_counts.clear() 
    for item in agent.inventory:
        inventory_counts[item] = inventory_counts.get(item, 0) + 1
    if len(agent.inventory) == 0:
        equipped_item_index = None
        equipped_item = None
    elif len(set(agent.inventory)) == 1:
        equipped_item_index = 0
        equipped_item = list(inventory_counts)[equipped_item_index]

    elif agent.inventory != []:
        if not equiped_islast:
            equipped_item = list(inventory_counts)[equipped_item_index]
        else: 
            try:
                equipped_item = list(inventory_counts)[equipped_item_index]
            except IndexError:
                equipped_item_index -= 1
                equipped_item = list(inventory_counts)[equipped_item_index]

    
    DISPLAY.blit(bottomBarImg,(0, HEIGHT*TILE_SIZE))
    x_pos = 10
    y_pos = (HEIGHT+BOTTOMBAR/2) * TILE_SIZE - 5

    for item, count in inventory_counts.items():
        text_color = (255, 255, 255) 
        if equipped_item_index is not None and count > 0 and item == list(inventory_counts.keys())[equipped_item_index]:
            text_color = (255, 0, 0)
        text = font.render(f"{item}: {count}", True, text_color)
        DISPLAY.blit(text, (x_pos, y_pos))
        x_pos += text.get_width() + 10


    texthelper = font.render("COORDS: 444.44, 444.44", True, (255, 255, 255))
    maxwidth = texthelper.get_width()
    textCords = font.render(f"COORDS: {agent.position.x}, {agent.position.y}", True, (255, 255, 255))
    DISPLAY.blit(textCords, (WIDTH * TILE_SIZE - maxwidth - 10, y_pos))




def tick():
    CLOCK.tick(FRAMERATE)
    world_map.render(DISPLAY, renderLeft, renderTop)
    agent.render(DISPLAY, renderLeft, renderTop)
    displayBar()
    if showEq:
        agent.render_Inv(DISPLAY)
    if paused:
        if ticks % 40 in range (0,30):
            DISPLAY.blit(pausedImg,(0, 0))
        DISPLAY.blit(pausedIcon,(0, 0))
        
        
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
    DISPLAY = pygame.display.set_mode(((WIDTH+RIGHTBAR) * TILE_SIZE, (HEIGHT+BOTTOMBAR) * TILE_SIZE))
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption('gierka')
    font = pygame.font.SysFont(None, 25, True, True)
    world_map = Map(WIDTH*MAP_SIZE, HEIGHT*MAP_SIZE, TILE_SIZE)
    agent = Agent(TILE_SIZE,world_map)
    is_running = True
    paused = False
    showEq = False
    ticks = 0
    equipped_item_index = None
    equiped_islast = True
    inventory_counts = {}

    while is_running:
        renderLeft, renderTop = updateCamera()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == KEYDOWN:
                if event.key == PAUSE_BT:
                    paused = not paused
                    ticks = 0
                elif not paused:
                    if event.key == SHOWEQ_BT:
                        showEq = not showEq
            elif event.type == pygame.MOUSEBUTTONDOWN and not paused:

                if event.button == 1:
                    clicked_x = int(math.floor(event.pos[0]/TILE_SIZE + renderLeft))
                    clicked_y = int(math.floor(event.pos[1]/TILE_SIZE + renderTop))
                    agent.destroy(clicked_x, clicked_y)
                elif event.button == 3:
                    clicked_x = int(math.floor(event.pos[0]/TILE_SIZE + renderLeft))
                    clicked_y = int(math.floor(event.pos[1]/TILE_SIZE + renderTop))
                    agent.place(equipped_item, clicked_x, clicked_y)


                elif event.button == 4:
                    if equipped_item_index is not None:
                        if equipped_item_index < len(set(agent.inventory)) - 1:
                            equipped_item_index += 1
                            equipped_item = list(inventory_counts)[equipped_item_index]

                elif event.button == 5:
                    if equipped_item_index is not None:
                        if equipped_item_index != 0:
                            equipped_item_index -= 1
                            equipped_item = list(inventory_counts)[equipped_item_index]
        if not showEq and not paused:
            keys = pygame.key.get_pressed()
            if keys[MOVEUP_BT]:
                agent.move('W', world_map)
            if keys[MOVEDOWN_BT]:
                agent.move('S', world_map)
            if keys[MOVELEFT_BT]:
                agent.move('A', world_map)
            if keys[MOVERIGHT_BT]:
                agent.move('D', world_map)

        tick()
        ticks += 1
    pygame.quit()
