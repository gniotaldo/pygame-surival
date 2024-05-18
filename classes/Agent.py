from pygame.math import Vector2
import pygame
from typing import List
from math import ceil,floor
from classes.Map import Map
from enum import Enum
from misc.config import HEIGHT, WIDTH, BAR, WALKINGSPEED1, SWIMMINGSPEED1
from misc.images import invBack, walkImages, swimImages

WALKINGSPEED = WALKINGSPEED1 / 10
SWIMMINGSPEED = SWIMMINGSPEED1 / 10

class Agent:

    class MovementType (Enum):
        Swimming = "Swimming"
        Walking = "Walking"

    def __init__(self, size: int, restaurant_map: Map):
        self._size = size
        self.map = restaurant_map
        self.position = self.getInitPosition()
        self.facing = Vector2(self.position.x,self.position.y+1)
        self.movement = self.MovementType.Walking
        self.image_index = 0
        self.speed = WALKINGSPEED/10.0
        self.prevSpeed = self.speed
        self.wood = 0
        self.rock = 0
        self.lily = 0
        self.iron = 0
        self.inventory = []
        

    def getInitPosition(self):
        for x in range (int(self.map._width/3),self.map._width):
            for y in range (int(self.map._height/3),self.map._height):
                if self.map.map_grid[x][y].type == Map.Item.ItemType.Grass:
                    return Vector2(x,y)
        return Vector2(0,0)


    def render(self, display, left, top):
        match self.movement:
            case self.MovementType.Swimming:
                images = swimImages
            case self.MovementType.Walking:
                images = walkImages
        display.blit(
            images[self.image_index],
            ((self.position.x - left) * self._size, (self.position.y - top) * self._size)
        )

    def render_Inv(self, display, buttons):

        ...


    def craft(self, item: Map.Item.ItemType):
        match item:
            case Map.Item.ItemType.Doors:
                if self.inventory.count("Wood") >= 6:
                    for _ in range(6):
                        self.inventory.remove("Wood")
                    self.inventory.append(item.name)
                    print("Wytworzono drzwi")
                else:
                    print("Za malo drewna")
                    ...
            case Map.Item.ItemType.Furnace:
                if self.inventory.count("Cobblestone") >= 8:
                    for _ in range(8):
                        self.inventory.remove("Cobblestone")
                    self.inventory.append(item.name)
                    print("Wytworzono piec")
                else:
                    print("Za malo cobbla")
                ...
            case Map.Item.ItemType.Glass:
                if self.inventory.count("Grass") >= 4:
                    for _ in range(4):
                        self.inventory.remove("Grass")
                    self.inventory.append(item.name)
                    print("Wytworzono szklo")
                else:
                    print("Za malo trawy")
                ...

        ...


    def addToInventory(self, item: Map.Item.ItemType):
            self.inventory.append(item.name)

    def isStandingOn(self,x,y):
        return ((floor(self.position.x) == x and floor(self.position.y) == y) or(
                floor(self.position.x) == x and ceil(self.position.y) == y) or(
                ceil(self.position.x) == x and floor(self.position.y) == y) or(
                ceil(self.position.x) == x and ceil(self.position.y) == y))


    def destroy(self, x: int, y: int):
        distance = ((x - self.position.x)**2 + (y - self.position.y)**2)**(1/2)
        if distance <= 3 and not self.isStandingOn(x,y):
            destroyingCell: Map.Item = self.map.map_grid[x][y]
            if destroyingCell.type.is_destroyable():
                self.addToInventory(destroyingCell.type.product())
                self.map.map_grid[x][y].type = self.map.map_grid[x][y].under
                self.map.map_grid[x][y].under = self.map.map_grid[x][y].under2
                self.map.map_grid[x][y].under2 = None
                if not self.map.map_grid[x][y].type.is_hole():
                    self.map.map_grid[x][y].isfloor = True
                else:
                    self.map.map_grid[x][y].isfloor = False
        self.inventory.sort()
                

    def place(self,object, x: int, y: int):
        distance = ((x - self.position.x)**2 + (y - self.position.y)**2)**(1/2)
        if object is not None and distance <= 4 and not self.isStandingOn(x,y):
            placingItem: Map.Item = Map.Item
            placingItem.type = getattr(Map.Item.ItemType, object)
            if placingItem.type.is_placable():
                if self.map.map_grid[x][y].type.is_enterable() or self.map.map_grid[x][y].isfloor:
                    self.map.map_grid[x][y].under2 = self.map.map_grid[x][y].under
                    self.map.map_grid[x][y].under = self.map.map_grid[x][y].type
                    self.map.map_grid[x][y].type = placingItem.type
                    self.map.map_grid[x][y].isfloor = False
                    self.inventory.remove(object)
                elif self.map.map_grid[x][y].type.is_hole():
                    self.map.map_grid[x][y].under2 = self.map.map_grid[x][y].under
                    self.map.map_grid[x][y].under = self.map.map_grid[x][y].type
                    self.map.map_grid[x][y].type = placingItem.type
                    self.map.map_grid[x][y].isfloor = True
                    self.inventory.remove(object)
            self.inventory.sort()

    
    def move(self,moveType, map: Map):
        if moveType == 'W':
            self.image_index = 2
            next_y = self.position.y - self.speed
            if next_y >= 0 and (
                                map.map_grid[ceil(self.position.x)][floor(next_y)].under is not None and
                                (map.map_grid[ceil(self.position.x)][floor(next_y)].under2 is None 
                                or map.map_grid[ceil(self.position.x)][floor(next_y)].type == Map.Item.ItemType.OpenDoors)
                                ) and (
                                map.map_grid[floor(self.position.x)][floor(next_y)].under is not None and
                                (map.map_grid[floor(self.position.x)][floor(next_y)].under2 is None
                                or map.map_grid[floor(self.position.x)][floor(next_y)].type == Map.Item.ItemType.OpenDoors)
                                ):
                if self.map.map_grid[int(ceil(self.position.x))][int(floor(self.position.y))].type == Map.Item.ItemType.Water and (
                self.map.map_grid[int(floor(self.position.x))][int(floor(self.position.y))].type == Map.Item.ItemType.Water) and (
                self.map.map_grid[int(ceil(self.position.x))][int(ceil(self.position.y))].type == Map.Item.ItemType.Water) and (
                self.map.map_grid[int(floor(self.position.x))][int(ceil(self.position.y))].type == Map.Item.ItemType.Water):
                    self.speed = SWIMMINGSPEED
                    self.movement = self.MovementType.Swimming
                    if self.prevSpeed != self.speed:
                        self.position.x = round(floor(self.position.x/SWIMMINGSPEED)*SWIMMINGSPEED,2)
                        self.position.y = round(floor(self.position.y/SWIMMINGSPEED-WALKINGSPEED)*SWIMMINGSPEED-WALKINGSPEED,2)
                else:
                    self.speed = WALKINGSPEED
                    self.movement = self.MovementType.Walking
                    if self.prevSpeed != self.speed:
                        self.position.x = round(round(self.position.x/WALKINGSPEED)*WALKINGSPEED,2)
                        self.position.y = round(round(self.position.y/WALKINGSPEED-SWIMMINGSPEED)*WALKINGSPEED-SWIMMINGSPEED,2)
                        next_y = round(next_y/WALKINGSPEED)*WALKINGSPEED
                
                self.position.y = round(next_y, 2)
            self.facing = Vector2(self.position.x, self.position.y - 1)
            
        elif moveType == 'S':
            self.image_index = 0
            next_y = self.position.y + self.speed
            if next_y <= self.map._height-1 and (
                                map.map_grid[ceil(self.position.x)][ceil(next_y)].under is not None and
                                (map.map_grid[ceil(self.position.x)][ceil(next_y)].under2 is None 
                                or map.map_grid[ceil(self.position.x)][ceil(next_y)].type == Map.Item.ItemType.OpenDoors)
                                ) and (
                                map.map_grid[floor(self.position.x)][ceil(next_y)].under is not None and
                                (map.map_grid[floor(self.position.x)][ceil(next_y)].under2 is None
                                or map.map_grid[floor(self.position.x)][ceil(next_y)].type == Map.Item.ItemType.OpenDoors)
                                ):
                if self.map.map_grid[int(ceil(self.position.x))][int(floor(self.position.y))].type == Map.Item.ItemType.Water and (
                self.map.map_grid[int(floor(self.position.x))][int(floor(self.position.y))].type == Map.Item.ItemType.Water) and (
                self.map.map_grid[int(ceil(self.position.x))][int(ceil(self.position.y))].type == Map.Item.ItemType.Water) and (
                self.map.map_grid[int(floor(self.position.x))][int(ceil(self.position.y))].type == Map.Item.ItemType.Water):
                    self.speed = SWIMMINGSPEED
                    self.movement = self.MovementType.Swimming
                    if self.prevSpeed != self.speed:
                        self.position.x = round(floor(self.position.x/SWIMMINGSPEED)*SWIMMINGSPEED,2)
                        self.position.y = round(floor(self.position.y/SWIMMINGSPEED+WALKINGSPEED)*SWIMMINGSPEED+WALKINGSPEED,2)
                else:
                    self.speed = WALKINGSPEED
                    self.movement = self.MovementType.Walking
                    if self.prevSpeed != self.speed:
                        self.position.x = round(round(self.position.x/WALKINGSPEED)*WALKINGSPEED,2)
                        self.position.y = round(round(self.position.y/WALKINGSPEED+SWIMMINGSPEED)*WALKINGSPEED+SWIMMINGSPEED,2)
                        next_y = round(next_y/WALKINGSPEED)*WALKINGSPEED
                
                self.position.y = round(next_y, 2)  # Zaokrąglanie do jednego miejsca po przecinku
            self.facing = Vector2(self.position.x, self.position.y + 1)
        elif moveType == 'A':
            self.image_index = 1
            next_x = self.position.x - self.speed
            if next_x >= BAR and  (
                                map.map_grid[floor(next_x)][ceil(self.position.y)].under is not None and
                                (map.map_grid[floor(next_x)][ceil(self.position.y)].under2 is None 
                                or map.map_grid[floor(next_x)][ceil(self.position.y)].type == Map.Item.ItemType.OpenDoors)
                                ) and (
                                map.map_grid[floor(next_x)][floor(self.position.y)].under is not None and
                                (map.map_grid[floor(next_x)][floor(self.position.y)].under2 is None
                                or map.map_grid[floor(next_x)][floor(self.position.y)].type == Map.Item.ItemType.OpenDoors)
                                ):
                if self.map.map_grid[int(ceil(self.position.x))][int(floor(self.position.y))].type == Map.Item.ItemType.Water and (
                self.map.map_grid[int(floor(self.position.x))][int(floor(self.position.y))].type == Map.Item.ItemType.Water) and (
                self.map.map_grid[int(ceil(self.position.x))][int(ceil(self.position.y))].type == Map.Item.ItemType.Water) and (
                self.map.map_grid[int(floor(self.position.x))][int(ceil(self.position.y))].type == Map.Item.ItemType.Water):
                    self.speed = SWIMMINGSPEED
                    self.movement = self.MovementType.Swimming
                    if self.prevSpeed != self.speed:
                        self.position.x = round(floor(self.position.x/SWIMMINGSPEED-WALKINGSPEED)*SWIMMINGSPEED-WALKINGSPEED,2)
                        self.position.y = round(floor(self.position.y/SWIMMINGSPEED)*SWIMMINGSPEED,2)
                else:
                    self.speed = WALKINGSPEED
                    self.movement = self.MovementType.Walking
                    if self.prevSpeed != self.speed:
                        self.position.x = round(round(self.position.x/WALKINGSPEED-SWIMMINGSPEED)*WALKINGSPEED-SWIMMINGSPEED,2)
                        self.position.y = round(round(self.position.y/WALKINGSPEED)*WALKINGSPEED,2)
                        next_x = round(next_x/WALKINGSPEED)*WALKINGSPEED
                
                self.position.x = round(next_x, 2)
            self.facing = Vector2(self.position.x - 1, self.position.y)
        elif moveType == 'D':
            self.image_index = 3
            next_x = self.position.x + self.speed
            if next_x <= self.map._width-1 and  (
                                map.map_grid[ceil(next_x)][ceil(self.position.y)].under is not None and
                                (map.map_grid[ceil(next_x)][ceil(self.position.y)].under2 is None 
                                or map.map_grid[ceil(next_x)][ceil(self.position.y)].type == Map.Item.ItemType.OpenDoors)
                                ) and (
                                map.map_grid[ceil(next_x)][floor(self.position.y)].under is not None and
                                (map.map_grid[ceil(next_x)][floor(self.position.y)].under2 is None
                                or map.map_grid[ceil(next_x)][floor(self.position.y)].type == Map.Item.ItemType.OpenDoors)
                                ):
                if self.map.map_grid[int(ceil(self.position.x))][int(floor(self.position.y))].type == Map.Item.ItemType.Water and (
                self.map.map_grid[int(floor(self.position.x))][int(floor(self.position.y))].type == Map.Item.ItemType.Water) and (
                self.map.map_grid[int(ceil(self.position.x))][int(ceil(self.position.y))].type == Map.Item.ItemType.Water) and (
                self.map.map_grid[int(floor(self.position.x))][int(ceil(self.position.y))].type == Map.Item.ItemType.Water):
                    self.speed = SWIMMINGSPEED
                    self.movement = self.MovementType.Swimming
                    if self.prevSpeed != self.speed:
                        self.position.x = round(floor(self.position.x/SWIMMINGSPEED+WALKINGSPEED)*SWIMMINGSPEED+WALKINGSPEED,2)
                        self.position.y = round(floor(self.position.y/SWIMMINGSPEED)*SWIMMINGSPEED,2)
                else:
                    self.speed = WALKINGSPEED
                    self.movement = self.MovementType.Walking
                    if self.prevSpeed != self.speed:
                        self.position.x = round(round(self.position.x/WALKINGSPEED+SWIMMINGSPEED)*WALKINGSPEED+SWIMMINGSPEED,2)
                        self.position.y = round(round(self.position.y/WALKINGSPEED)*WALKINGSPEED,2)
                        next_x = round(next_x/WALKINGSPEED)*WALKINGSPEED
                
                self.position.x = round(next_x, 2)
        self.facing = Vector2(self.position.x + 1, self.position.y)
        self.prevSpeed = self.speed
