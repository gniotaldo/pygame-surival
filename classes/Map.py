import math
import random
from enum import Enum
import pygame
from typing import List
from pygame.math import Vector2
from misc.images import grass_cell
from misc.config import BAR, CHUNK_SIZE


class Chunk:

    class ChunkTypes(Enum):
        Forrest = 'F'
        Lake = 'L'
        Mountains = 'M'

    def __init__(self, type, topleftX, topleftY, tile_size, world_map: 'Map'):
        self.positions = [] 
        self.type = type
        self.map = world_map
        self.objects = []
        for x in range (topleftX, topleftX + CHUNK_SIZE):
            if x >= 0 and x < world_map._width:
                for y in range (topleftY, topleftY + CHUNK_SIZE):
                    if y >= 0 and y < world_map._height:
                        self.positions.append((x,y))
                    else:
                        break
            else:
                break
        self._tile_size = tile_size
        self.set_chunk()


    def set_chunk(self):
        match self.type:
            case self.ChunkTypes.Forrest:
                self.generateForrest()
            case self.ChunkTypes.Lake:
                self.generateLake()
            case self.ChunkTypes.Mountains:
                self.generateMountains()

    def generateForrest(self):
        print("robie las")
        for x, y in self.positions:
            randomizer = random.randint(0,10)
            if randomizer in range (0,8):
                self.map.map_grid[x][y] = Map.Cell.GrassCell
            else:
                self.map.map_grid[x][y] = Map.Cell.TreeCell
                self.map.tree_cells.append((x,y))

    def generateLake(self):
        print("robie jezioro")
        for x, y in self.positions:
            randomizer = random.randint(0,10)
            if randomizer == 0:
                self.map.map_grid[x][y] = Map.Cell.LilyCell
                self.map.lily_cells.append((x,y))
            else:
                self.map.map_grid[x][y] = Map.Cell.WaterCell
                self.map.water_cells.append((x,y))

    def generateMountains(self):
        print("robie gory")
        for x, y in self.positions:
            randomizer = random.randint(0,10)
            if randomizer == 0:
                self.map.map_grid[x][y] = Map.Cell.IronOreCell
                self.map.ironOre_cells.append((x,y))
            else:
                self.map.map_grid[x][y] = Map.Cell.RockCell
                self.map.rock_cells.append((x,y))




class Map:
    class Cell(Enum):
        GrassCell = "Grass"
        TreeCell = "Tree"
        WaterCell = "Lake"
        RockCell = "Rock"
        LilyCell = "Lily"
        IronOreCell = "IronOre"
    
        def is_enterable(self):
            enterable_cells = [self.GrassCell, self.LilyCell]
            return self in enterable_cells


    def __init__(self, width, height, tile_size):
        self.map_grid: List[List[self.Cell]] = None
        self._width = width
        self._height = height
        self._tile_size = tile_size
        self.chunks = []
        self.tree_cells = []
        self.lily_cells = []
        self.ironOre_cells = []
        self.water_cells = []
        self.rock_cells = []
        self.set_map()

    def set_map(self):
        self.map_grid = [[self.Cell.GrassCell for _ in range(self._height)] for _ in range(self._width)]
        #self.set_trees()
        self.set_chunks()

    def set_chunks(self):
        chunkId = 0
        for x in range (self._width):
            if x % CHUNK_SIZE == 0:
                for y in range (self._height):
                    if y % CHUNK_SIZE == 0:
                        randomTypeId = random.randint(0,2)
                        match randomTypeId:
                            case 0:
                                chunk_type = Chunk.ChunkTypes.Forrest
                            case 1:
                                chunk_type = Chunk.ChunkTypes.Lake
                            case 2:
                                chunk_type = Chunk.ChunkTypes.Mountains
                        chunk = Chunk(chunk_type,x,y,self._tile_size,self)
                        self.chunks.append(chunk)
                        chunkId += 1

    def set_trees(self):
        attempt = 0
        while attempt < 30:
            random_x = random.randint(BAR, self._width - 1)
            random_y = random.randint(BAR, self._height - 1)
            if self.map_grid[random_x][random_y] != self.Cell.TreeCell and not any(
                    math.sqrt((random_x - tx) ** 2 + (random_y - ty) ** 2) <= 4 for tx, ty in self.tree_cells
            ):
                self.tree_cells.append((random_x, random_y))

            else:
                attempt += 1
        for x, y in self.tree_cells:
            self.map_grid[x][y] = self.Cell.TreeCell


    def render(self, display):
        for y in range(self._height):
            for x in range(self._width):
                display.blit(
                    grass_cell,
                    (x * self._tile_size, y * self._tile_size)
                )
