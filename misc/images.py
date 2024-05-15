import pygame.locals
from misc.config import TILE_SIZE, BAR, HEIGHT, WIDTH, BOTTOMBAR
import pygame

size=TILE_SIZE

swimS=pygame.transform.scale(pygame.image.load("images/swimS.png"),(size, size))
swimW=pygame.transform.scale(pygame.image.load("images/swimW.png"),(size, size))
swimN=pygame.transform.scale(pygame.image.load("images/swimN.png"),(size, size))
swimE=pygame.transform.scale(pygame.image.load("images/swimE.png"),(size, size))
swimImages = [swimS, swimW, swimN, swimE]


walkS=pygame.transform.scale(pygame.image.load("images/walkS.png"),(size, size))
walkW=pygame.transform.scale(pygame.image.load("images/walkW.png"),(size, size))
walkN=pygame.transform.scale(pygame.image.load("images/walkN.png"),(size, size))
walkE=pygame.transform.scale(pygame.image.load("images/walkE.png"),(size, size))
walkImages = [walkS, walkW, walkN, walkE]


#cell images
tree_cell = pygame.transform.scale( pygame.image.load("images/tree.png"),  (size, size))
water_cell = pygame.transform.scale( pygame.image.load("images/water.png"),  (size, size))
rock_cell = pygame.transform.scale( pygame.image.load("images/rock.png"),  (size, size))
grass_cell = pygame.transform.scale(pygame.image.load("images/grass.png"),  (size, size))
ironOre_cell = pygame.transform.scale(pygame.image.load("images/ironOre.png"),  (size, size))
lily_cell = pygame.transform.scale(pygame.image.load("images/lily.png"),  (size, size))
rockFloor_cell = pygame.transform.scale(pygame.image.load("images/rockFloor.png"),  (size, size))
cobblestone_cell =pygame.transform.scale(pygame.image.load("images/cobblestone.png"),  (size, size))
wood_cell = pygame.transform.scale(pygame.image.load("images/wood.png"),  (size, size))
dirt_cell = pygame.transform.scale(pygame.image.load("images/dirt.png"),  (size, size))
rockhole_cell = pygame.transform.scale(pygame.image.load("images/rockhole.png"),  (size, size))
floorImg = pygame.transform.scale(pygame.image.load("images/floor.png"),  (size, size))
wallImg = pygame.transform.scale(pygame.image.load("images/wall.png"),  (size, size))


barImg = pygame.transform.scale(pygame.image.load("images/bar.png"), (size * BAR, size * HEIGHT))
bottomBarImg = pygame.transform.scale(pygame.image.load("images/bottomBar.png"),(size * WIDTH, size * BOTTOMBAR))
invBack = pygame.transform.scale(pygame.image.load("images/inventory_background.png"), (size * WIDTH, size * HEIGHT))
pausedImg = pygame.transform.scale(pygame.image.load("images/paused.png"), (size * WIDTH, size * HEIGHT))
pausedIcon = pygame.image.load("images/pauseIcon.png")