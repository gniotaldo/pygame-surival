import pygame
from pygame.math import Vector2
from misc.images import tree_cell

class Tree:
    def __init__(self, position: Vector2, size: int, map_width: int, map_height: int):
        self.position = position
        self._table_image = tree_cell
        self._size = size
        self.map_width = map_width
        self.map_height = map_height

    def render(self, display, left, top):
        display.blit(
            self._table_image,
            ((self.position.x-left) * self._size, (self.position.y-top) * self._size)
        )