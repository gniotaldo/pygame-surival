import math
import random
from enum import Enum
import pygame
from typing import List
from pygame.math import Vector2
from misc.images import grass_cell, rockFloor_cell
from misc.config import BAR, CHUNK_SIZE, SEALEVEL

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


class Chunk:

    class ChunkTypes(Enum):
        Forrest = 'F'
        Lake = 'L'
        Mountains = 'M'

    def __init__(self, type, positions, tile_size, world_map: 'Map'):
        self.positions = positions 
        self.type = type
        self.map = world_map
        self.objects = []
        '''
        for x in range (topleftX, topleftX + CHUNK_SIZE):
            if x >= 0 and x < world_map._width:
                for y in range (topleftY, topleftY + CHUNK_SIZE):
                    if y >= 0 and y < world_map._height:
                        self.positions.append((x,y))
                    else:
                        break
            else:
                break
        '''
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
        for x, y in self.positions:
            randomizer = random.randint(0,10)
            if randomizer in range (0,8):
                self.map.map_grid[x][y] = Map.Cell.GrassCell
            else:
                self.map.map_grid[x][y] = Map.Cell.TreeCell
                self.map.tree_cells.append((x,y))

    def generateLake(self):
        for x, y in self.positions:
            randomizer = random.randint(0,10)
            if randomizer == 0:
                self.map.map_grid[x][y] = Map.Cell.LilyCell
                self.map.lily_cells.append((x,y))
            else:
                self.map.map_grid[x][y] = Map.Cell.WaterCell
                self.map.water_cells.append((x,y))

    def generateMountains(self):
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
        RockFloorCell = "RockFloor"
        WaterCell = "Lake"

        TreeCell = "Tree"
        RockCell = "Rock"
        LilyCell = "Lily"
        IronOreCell = "IronOre"
    
        def is_enterable(self):
            enterable_cells = [self.GrassCell, self.LilyCell, self.RockFloorCell]
            return self in enterable_cells
    
        def is_destroyable(self):
            destroyable_cells = [self.TreeCell, self.RockCell, self.LilyCell, self.IronOreCell]
            return self in destroyable_cells
        def floor(self):
            match self:
                case self.TreeCell:
                    return self.GrassCell
                case self.LilyCell:
                    return self.WaterCell
                case self.RockCell:
                    return self.RockFloorCell
                case self.IronOreCell:
                    return self.RockFloorCell
                case _:
                    return self.GrassCell
                    
    def imageForCell(self, cell: Cell):
        if cell == self.Cell.RockFloorCell:
            return rockFloor_cell
        else:
            return grass_cell
    def __init__(self, width, height, tile_size):
        #seed = random.randint(0,70)
        seed = 20
        map_gen = MapGenerator(width, height, 100.0, 6, 0.5, 2.0, seed)
        self.world_map = map_gen.generate_map()
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
        self.map_grid = [[self.Cell.GrassCell for _ in range(self._height)] for _ in range(self._width)]
        las = Chunk(Chunk.ChunkTypes.Forrest,self.forrestPos,self._tile_size,self)
        self.chunks.append(las)
        jezioro = Chunk(Chunk.ChunkTypes.Lake,self.lakePos,self._tile_size,self)
        self.chunks.append(jezioro)
        gory = Chunk(Chunk.ChunkTypes.Mountains,self.mountainsPos,self._tile_size,self)
        self.chunks.append(gory)

    def render(self, display):
        for y in range(self._height):
            for x in range(self._width):
                display.blit(
                    self.imageForCell(self.map_grid[x][y]),
                    (x * self._tile_size, y * self._tile_size)
                )
