import pygame
from pygame.math import Vector2
from misc.images import lily_cell

class Lily:
    def __init__(self, position: Vector2, size: int, map_width: int, map_height: int):
        self.position = position
        self._table_image = lily_cell
        self._size = size
        self.map_width = map_width
        self.map_height = map_height

    def render(self, display):
        display.blit(
            self._table_image,
            (self.position.x * self._size, self.position.y * self._size)
        )