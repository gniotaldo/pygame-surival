from misc.config import TILE_SIZE, BAR, HEIGHT, WIDTH, BOTTOMBAR
import pygame

size=TILE_SIZE

kelS=pygame.transform.scale(pygame.image.load("images/kelS.png"),(size, size))
kelW=pygame.transform.scale(pygame.image.load("images/kelW.png"),(size, size))
kelN=pygame.transform.scale(pygame.image.load("images/kelN.png"),(size, size))
kelE=pygame.transform.scale(pygame.image.load("images/kelE.png"),(size, size))
waiterImgs = [kelS, kelW, kelN, kelE]

tree_cell = pygame.transform.scale( pygame.image.load("images/tree.png"),  (size, size))
water_cell = pygame.transform.scale( pygame.image.load("images/water.png"),  (size, size))
rock_cell = pygame.transform.scale( pygame.image.load("images/rock.png"),  (size, size))
grass_cell = pygame.transform.scale(pygame.image.load("images/grass.png"),  (size, size))
ironOre_cell = pygame.transform.scale(pygame.image.load("images/ironOre.png"),  (size, size))
lily_cell = pygame.transform.scale(pygame.image.load("images/lily.png"),  (size, size))
rockFloor_cell = pygame.transform.scale(pygame.image.load("images/rockFloor.png"),  (size, size))

barImg = pygame.transform.scale(pygame.image.load("images/bar.png"), (size * BAR, size * HEIGHT))
bottomBarImg = pygame.transform.scale(pygame.image.load("images/bottomBar.png"),(size * WIDTH, size * BOTTOMBAR))