from pygame.math import Vector2
import pygame
from typing import List
from math import ceil,floor
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
        for x in range (int(self.map._width/3),self.map._width):
            for y in range (int(self.map._height/3),self.map._height):
                if self.map.map_grid[x][y] == Map.Cell.GrassCell:
                    return Vector2(x,y)
        return Vector2(0,0)


    def render(self, display, left, top):
        display.blit(
            self._waiter_image,
            ((self.position.x - left) * self._size, (self.position.y - top) * self._size)
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
        #ff
        facingCell: Map.Cell = self.map.map_grid[floor(self.facing.x)][floor(self.facing.y)]
        found = False
        if facingCell.is_destroyable():
            for object in objects:
                if int(object.position.x) == int(floor(self.facing.x)) and int(object.position.y) == int(floor(self.facing.y)):
                    objects.remove(object)
                    found = True
                    break
            self.map.map_grid[floor(self.facing.x)][floor(self.facing.y)] = facingCell.floor()
            self.addToInventory(facingCell)
        #cc
        if not found:
            facingCell: Map.Cell = self.map.map_grid[ceil(self.facing.x)][ceil(self.facing.y)]
            if facingCell.is_destroyable():
                for object in objects:
                    if int(object.position.x) == int(ceil(self.facing.x)) and int(object.position.y) == int(ceil(self.facing.y)):
                        objects.remove(object)
                        found = True
                        break
                self.map.map_grid[ceil(self.facing.x)][ceil(self.facing.y)] = facingCell.floor()
                self.addToInventory(facingCell)
        #fc
        if not found:
            facingCell: Map.Cell = self.map.map_grid[floor(self.facing.x)][ceil(self.facing.y)]
            if facingCell.is_destroyable():
                for object in objects:
                    if int(object.position.x) == int(floor(self.facing.x)) and int(object.position.y) == int(ceil(self.facing.y)):
                        objects.remove(object)
                        found = True
                        break
                self.map.map_grid[floor(self.facing.x)][ceil(self.facing.y)] = facingCell.floor()
                self.addToInventory(facingCell)
        #cf
        if not found:
            facingCell: Map.Cell = self.map.map_grid[ceil(self.facing.x)][floor(self.facing.y)]
            if facingCell.is_destroyable():
                for object in objects:
                    if int(object.position.x) == int(ceil(self.facing.x)) and int(object.position.y) == int(floor(self.facing.y)):
                        objects.remove(object)
                        found = True
                        break
                self.map.map_grid[ceil(self.facing.x)][floor(self.facing.y)] = facingCell.floor()
                self.addToInventory(facingCell)


    def place(self, item):
        if item > 0:
            ...


    
    def move(self,moveType, map: Map):
        if moveType == 'W':
            self._waiter_image = dirImgs[2]
            next_y = self.position.y - 0.2
            if next_y >= 0 and map.map_grid[ceil(self.position.x)][floor(next_y)].is_enterable() and map.map_grid[floor(self.position.x)][floor(next_y)].is_enterable():
                self.position.y = round(next_y, 1)  # Zaokrąglanie do jednego miejsca po przecinku
            self.facing = Vector2(self.position.x, self.position.y - 1)
        elif moveType == 'S':
            self._waiter_image = dirImgs[0]
            next_y = self.position.y + 0.2
            if next_y < self.map._height and map.map_grid[ceil(self.position.x)][ceil(next_y)].is_enterable() and map.map_grid[floor(self.position.x)][ceil(next_y)].is_enterable():
                self.position.y = round(next_y, 1)
            self.facing = Vector2(self.position.x, self.position.y + 1)
        elif moveType == 'A':
            self._waiter_image = dirImgs[1]
            next_x = self.position.x - 0.2
            if next_x >= BAR and map.map_grid[floor(next_x)][ceil(self.position.y)].is_enterable() and map.map_grid[floor(next_x)][floor(self.position.y)].is_enterable():
                self.position.x = round(next_x, 1)
            self.facing = Vector2(self.position.x - 1, self.position.y)
        elif moveType == 'D':
            self._waiter_image = dirImgs[3]
            next_x = self.position.x + 0.2
            if next_x < self.map._width and map.map_grid[ceil(next_x)][ceil(self.position.y)].is_enterable() and map.map_grid[ceil(next_x)][floor(self.position.y)].is_enterable():
                self.position.x = round(next_x, 1)
            self.facing = Vector2(self.position.x + 1, self.position.y)
