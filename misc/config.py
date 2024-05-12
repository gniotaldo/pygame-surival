import pygame

TILE_SIZE = 40
WIDTH = 30
HEIGHT = 20
MAP_SIZE = 10
FRAMERATE = 10
BAR=0
RIGHTBAR = 0
BOTTOMBAR = 2
CHUNK_SIZE = 5
SEALEVEL = 0 # (-5,5)


DISPLAY = pygame.display.set_mode(((WIDTH+RIGHTBAR) * TILE_SIZE, (HEIGHT+BOTTOMBAR) * TILE_SIZE))
CLOCK = pygame.time.Clock()
pygame.display.set_caption('gierka')