import math
import random
from enum import Enum
import pygame
from typing import List
from pygame.math import Vector2
from misc.images import *
from misc.config import BAR, SEALEVEL

import noise
import numpy as np

class MapGenerator:
    def __init__(self, width, height, scale, octaves, persistence, lacunarity, seed=None):
        self.width = width
        self.height = height
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.seed = seed
    
    def generate_map(self):
        if self.seed is not None:
            np.random.seed(self.seed)
            seed = np.random.randint(0, 100)
        else:
            seed = None

        world_map = np.zeros((self.width, self.height))

        for x in range(self.width):
            for y in range(self.height):
                world_map[x][y] = noise.pnoise2(x / self.scale, 
                                                y / self.scale, 
                                                octaves=self.octaves, 
                                                persistence=self.persistence, 
                                                lacunarity=self.lacunarity, 
                                                repeatx=self.width, 
                                                repeaty=self.height, 
                                                base=seed)

        return world_map


class Biome:

    class BiomeTypes(Enum):
        Forrest = 'F'
        Lake = 'L'
        Mountains = 'M'

    def __init__(self, type, positions, tile_size, world_map: 'Map'):
        self.positions = positions 
        self.type = type
        self.map = world_map
        self.objects = []
        self._tile_size = tile_size
        self.set_biome()


    def set_biome(self):
        match self.type:
            case self.BiomeTypes.Forrest:
                self.generateForrest()
            case self.BiomeTypes.Lake:
                self.generateLake()
            case self.BiomeTypes.Mountains:
                self.generateMountains()

    def generateForrest(self):
        for x, y in self.positions:
            randomizer = random.randint(0,10)
            if randomizer == 0:
                self.map.map_grid[x][y].type = Map.Item.ItemType.Tree
                self.map.map_grid[x][y].under = Map.Item.ItemType.Grass
                self.map.map_grid[x][y].under2 = Map.Item.ItemType.Dirt
            else:
                self.map.map_grid[x][y].type = Map.Item.ItemType.Grass
                self.map.map_grid[x][y].under = Map.Item.ItemType.Dirt

    def generateLake(self):
        for x, y in self.positions:
            randomizer = random.randint(0,10)
            if randomizer == 0:
                self.map.map_grid[x][y].type = Map.Item.ItemType.Lily
                self.map.map_grid[x][y].under = Map.Item.ItemType.Water
                self.map.map_grid[x][y].under2 = Map.Item.ItemType.Dirt
            else:
                self.map.map_grid[x][y].type = Map.Item.ItemType.Water
                self.map.map_grid[x][y].under = Map.Item.ItemType.Dirt
                self.map.water_cells.append((x,y))

    def generateMountains(self):
        for x, y in self.positions:
            randomizer = random.randint(0,10)
            if randomizer == 0:
                self.map.map_grid[x][y].type = Map.Item.ItemType.IronOre
                self.map.map_grid[x][y].under = Map.Item.ItemType.RockFloor
                self.map.ironOre_cells.append((x,y))
            else:
                self.map.map_grid[x][y].type = Map.Item.ItemType.Rock
                self.map.map_grid[x][y].under = Map.Item.ItemType.RockFloor
                self.map.rock_cells.append((x,y))
            self.map.map_grid[x][y].under2 = Map.Item.ItemType.RockHole




class Map:
    class Item:
        def __init__(self):
            self.type = self.ItemType.Grass
            self.under = self.ItemType.Dirt
            self.hovered = False
            self.under2 = None
            self.isfloor = False


        class ItemType(Enum):
            Grass = "Grass"
            RockFloor = "RockFloor"
            Water = "Water"

            Dirt = "Dirt"
            RockHole = "RockHole"

            Tree = "Tree"
            Rock = "Rock"
            Lily = "Lily"
            IronOre = "IronOre"

            Wood = "Wood"
            Cobblestone = "Cobblestone"
            IronOreShard = "IronOreShard"

            Air = "Air"

            Doors = "Doors"
            OpenDoors = "OpenDoors"
            Furnace = "Furnace"
            Glass = "Glass"

    
            def is_enterable(self):
                enterable_cells = [self.OpenDoors, self.Grass, self.Lily, self.RockFloor, self.OpenDoors]
                return self in enterable_cells
            
            def is_hole(self):
                holes = [self.Dirt, self.RockHole]
                return self in holes

            def is_destroyable(self):
                destroyable_items = [self.Doors, self.Furnace, self.Glass, self.Tree, self.Rock, self.Lily, self.IronOre, self.Wood, self.Cobblestone, self.Grass, self.RockFloor]
                return self in destroyable_items
            
            def is_swimmable(self):
                return self == self.Water

            def is_placable(self):
                placable_items = [self.Doors, self.Furnace, self.Glass, self.Wood, self.Cobblestone, self.Rock, self.Lily, self.RockFloor, self.Grass]
                return self in placable_items
            def is_transparent(self):
                return self in [self.Doors, self.Glass, self.OpenDoors]

            def floor(self):
                match self:
                    case self.Lily:
                        return self.Water
                    case self.RockFloor:
                        return self.RockHole
                    case self.Grass:
                        return self.Dirt
                    case _:
                        return None

            def product(self):
                match self:
                    case self.Tree:
                        return self.Wood
                    case self.Lily:
                        return self.Lily
                    case self.Rock:
                        return self.Cobblestone
                    case self.IronOre:
                        return self.IronOreShard
                    case _:
                        return self
                                
    def imageForCell(self, cellType:Item.ItemType, cell: Item):
        if cellType == self.Item.ItemType.Grass:
            return grass_cell
        elif cellType == self.Item.ItemType.RockFloor:
            return rockFloor_cell
        elif cellType == self.Item.ItemType.Water:
            return water_cell
        elif cellType == self.Item.ItemType.Tree:
            return tree_cell
        elif cellType == self.Item.ItemType.Rock:
            return rock_cell
        elif cellType == self.Item.ItemType.Lily:
            return lily_cell
        elif cellType == self.Item.ItemType.IronOre:
            return ironOre_cell
        elif cellType == self.Item.ItemType.Wood:
            return wood_cell
        elif cellType == self.Item.ItemType.Cobblestone:
            return cobblestone_cell
        elif cellType == self.Item.ItemType.Dirt:
            return dirt_cell
        elif cellType == self.Item.ItemType.RockHole:
            return rockhole_cell
        elif cellType == self.Item.ItemType.Furnace:
            return furnace_cell
        else:
            return self.imageForCell(cell.under, cell)
        
    def imageForTransparentCell(self, cell: Item.ItemType):
        if cell == self.Item.ItemType.Doors:
            return door_cell
        elif cell == self.Item.ItemType.OpenDoors:
            return openDoor_cell
        elif cell == self.Item.ItemType.Glass:
            return glass_cell

    def __init__(self, width, height, tile_size, RANDOMSEED, SEED, MAP_SIZE, SEALEVEL):
        if RANDOMSEED:
            seed = random.randint(0,70)
        else:
            seed = SEED
        map_gen = MapGenerator(width, height, 100.0, 6, 0.5, 2.0, seed)
        self.MAP_SIZE = MAP_SIZE
        self.world_map = map_gen.generate_map()
        self.map_grid: List[List[self.Item]] = None
        self._width = width
        self._height = height
        self._tile_size = tile_size
        self.chunks = []
        self.tree_cells = []
        self.lily_cells = []
        self.ironOre_cells = []
        self.water_cells = []
        self.rock_cells = []
        self.forrestPos = []
        self.mountainsPos = []
        self.lakePos = []
        self.world_map[0][0] = self.world_map[0][1]
        for x in range (0,self._width):
            for y in range (0,self._height):
                if self.world_map[x][y] > 0.15 - SEALEVEL/20:
                    self.mountainsPos.append((x,y))
                elif self.world_map[x][y] < 0 - SEALEVEL/20:
                    self.lakePos.append((x,y))
                elif self.world_map[x][y] > 0.05 - SEALEVEL/20:
                    self.forrestPos.append((x,y))
        self.set_map()

    def set_map(self):
        self.map_grid = [[self.Item() for _ in range(self._height)] for _ in range(self._width)]
        las = Biome(Biome.BiomeTypes.Forrest,self.forrestPos,self._tile_size,self)
        self.chunks.append(las)
        jezioro = Biome(Biome.BiomeTypes.Lake,self.lakePos,self._tile_size,self)
        self.chunks.append(jezioro)
        gory = Biome(Biome.BiomeTypes.Mountains,self.mountainsPos,self._tile_size,self)
        self.chunks.append(gory)

    def render(self, display, left, top):
        global HEIGHT, WIDTH
        endTop = min (int(top) + HEIGHT+2, 20*self.MAP_SIZE)
        endLeft =  min (int(left) + WIDTH+2, 20*self.MAP_SIZE)
        for y in range(int(top)-2, endTop):
            for x in range(int(left)-2, endLeft):
                display.blit(
                    self.imageForCell(self.map_grid[x][y].type, self.map_grid[x][y]),
                    ((x - left) * self._tile_size, (y - top) * self._tile_size)
                )
                if self.map_grid[x][y].type.is_transparent():
                    display.blit(
                        self.imageForTransparentCell(self.map_grid[x][y].type),
                        ((x - left) * self._tile_size, (y - top) * self._tile_size)
                    )
                if self.map_grid[x][y].hovered:
                    display.blit(
                        hoveredImg,
                        ((x - left) * self._tile_size, (y - top) * self._tile_size)
                    )

                if self.map_grid[x][y].type not in [self.Item.ItemType.Water, self.Item.ItemType.Grass] and self.map_grid[x][y].under2 is None and self.map_grid[x][y].under is not None:
                    display.blit(
                        floorImg,
                        ((x - left) * self._tile_size, (y - top) * self._tile_size)
                    )
                if self.map_grid[x][y].type not in [self.Item.ItemType.Doors, self.Item.ItemType.OpenDoors, self.Item.ItemType.Rock, self.Item.ItemType.IronOre, self.Item.ItemType.Tree, self.Item.ItemType.Lily] and self.map_grid[x][y].under2 is not None:
                    display.blit(
                        wallImg,
                        ((x - left) * self._tile_size, (y - top) * self._tile_size)
                    )

