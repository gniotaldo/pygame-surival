from pygame.math import Vector2
import pygame
from typing import List
from classes.Map import Map
from misc.config import HEIGHT,WIDTH,BAR
from misc.images import waiterImgs as dirImgs


class Agent:


    def __init__(self, size: int, restaurant_map: Map):
        self.map = restaurant_map
        self.position = self.getInitPosition()
        self.facing = Vector2(self.position.x,self.position.y+1)
        self._waiter_image = dirImgs[0]
        self._size = size
        self.status = 0 #0-idle, 1-going to client 2-idle but memory is full 3-going to kichen
        self.memorySize = 5
        self.inMemory = 0
        self.inHands = 0
        self.handsMax = 3

    def getInitPosition(self):
        for x in range (self.map._width):
            for y in range (self.map._height):
                if self.map.map_grid[x][y] == Map.Cell.GrassCell:
                    return Vector2(x,y)
        return Vector2(0,0)


    def render(self, display):
        display.blit(
            self._waiter_image,
            (self.position.x * self._size, self.position.y * self._size)
        )
    
    def move(self,moveType, map: Map):
        
        if moveType=='W':
            self._waiter_image = dirImgs[2]
            if (self.position.y>0 and map.map_grid[int(self.position.x)][int(self.position.y-1)] == Map.Cell.GrassCell):
                self.position.y -= 1
            self.facing = Vector2(self.position.x,self.position.y-1)
            if self.position.y == 0:
                self.facing = Vector2(self.position.x,self.position.y)
        elif moveType=='S':
            self._waiter_image = dirImgs[0]
            if (self.position.y<HEIGHT-1 and map.map_grid[int(self.position.x)][int(self.position.y+1)] == Map.Cell.GrassCell):
                self.position.y += 1
            self.facing = Vector2(self.position.x,self.position.y+1)
            if self.position.y == HEIGHT-1:
                self.facing = Vector2(self.position.x,self.position.y)
        elif moveType=='A':
            self._waiter_image = dirImgs[1]
            if (self.position.x>BAR and map.map_grid[int(self.position.x-1)][int(self.position.y)] == Map.Cell.GrassCell):
                self.position.x -= 1
            self.facing = Vector2(self.position.x-1,self.position.y)
            if self.position.x == 0:
                self.facing = Vector2(self.position.x,self.position.y)
        elif moveType=='D':
            self._waiter_image = dirImgs[3]
            if (self.position.x<WIDTH-1 and map.map_grid[int(self.position.x+1)][int(self.position.y)] == Map.Cell.GrassCell):
                self.position.x += 1
            self.facing = Vector2(self.position.x+1,self.position.y)
            if self.position.x == WIDTH-1:
                self.facing = Vector2(self.position.x,self.position.y)
    