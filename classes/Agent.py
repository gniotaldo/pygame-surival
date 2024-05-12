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
        self.wood = 0
        self.rock = 0
        self.lily = 0
        self.iron = 0
        self.inventory = []
        

    def getInitPosition(self):
        print(self.map._height, self.map._width)
        for x in range (0,self.map._width):
            for y in range (0,self.map._height):
                if self.map.map_grid[x][y] == Map.Cell.GrassCell:
                    return Vector2(x,y)
        return Vector2(0,0)


    def render(self, display):
        display.blit(
            self._waiter_image,
            (self.position.x * self._size, self.position.y * self._size)
        )

    def addToInventory(self, item: Map.Cell):
            self.inventory.append(item.name.replace("Cell", ""))
            match item:
                case Map.Cell.IronOreCell:
                    self.iron += 1
                case Map.Cell.TreeCell:
                    self.wood += 1
                case Map.Cell.RockCell:
                    self.rock += 1
                case Map.Cell.LilyCell:
                    self.lily += 1
                case _:
                    pass

    def destroy(self,objects: list[any]):
        facingCell: Map.Cell = self.map.map_grid[int(self.facing.x)][int(self.facing.y)]
        if facingCell.is_destroyable():
            for object in objects:
                if object.position == self.facing:
                    objects.remove(object)
                    break
            self.map.map_grid[int(self.facing.x)][int(self.facing.y)] = facingCell.floor()
            self.addToInventory(facingCell)

    def place(self, item):
        if item > 0:
            ...


    
    def move(self,moveType, map: Map):
        
        if moveType=='W':
            self._waiter_image = dirImgs[2]
            if (self.position.y>0 and map.map_grid[int(self.position.x)][int(self.position.y-1)].is_enterable()):
                self.position.y -= 1
            self.facing = Vector2(self.position.x,self.position.y-1)
            if self.position.y == 0:
                self.facing = Vector2(self.position.x,self.position.y)
        elif moveType=='S':
            self._waiter_image = dirImgs[0]
            if (self.position.y<HEIGHT-1 and map.map_grid[int(self.position.x)][int(self.position.y+1)].is_enterable()):
                self.position.y += 1
            self.facing = Vector2(self.position.x,self.position.y+1)
            if self.position.y == HEIGHT-1:
                self.facing = Vector2(self.position.x,self.position.y)
        elif moveType=='A':
            self._waiter_image = dirImgs[1]
            if (self.position.x>BAR and map.map_grid[int(self.position.x-1)][int(self.position.y)].is_enterable()):
                self.position.x -= 1
            self.facing = Vector2(self.position.x-1,self.position.y)
            if self.position.x == 0:
                self.facing = Vector2(self.position.x,self.position.y)
        elif moveType=='D':
            self._waiter_image = dirImgs[3]
            if (self.position.x<WIDTH-1 and map.map_grid[int(self.position.x+1)][int(self.position.y)].is_enterable()):
                self.position.x += 1
            self.facing = Vector2(self.position.x+1,self.position.y)
            if self.position.x == WIDTH-1:
                self.facing = Vector2(self.position.x,self.position.y)
        
    