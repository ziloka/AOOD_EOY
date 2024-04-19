# py -m pip install perlin-noise pygame
import random
import pygame
import sys
from pygame.locals import *

from consts import *
from render import CameraGroup, Player
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((TILES_COLUMN * TILE_SIZE, TILES_ROW * TILE_SIZE),  pygame.RESIZABLE)
SEED = random.randint(0, 100000)

camera_group = CameraGroup()
player = Player((640,360), camera_group)

while True:
    clock.tick(60)
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                pygame.quit()
                sys.exit()
            case pygame.WINDOWRESIZED:
                width, height = screen.get_width(), screen.get_height()
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            case pygame.MOUSEWHEEL:
                camera_group.zoom_scale += event.y * 0.03

    camera_group.update()
    camera_group.custom_draw(player)
    
    pygame.display.update()
