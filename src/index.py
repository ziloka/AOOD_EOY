# py -m pip install perlin-noise pygame
import sys
import pygame
from pygame.locals import *

from consts import *
from render import CameraGroup, Player
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((TILES_COLUMN * TILE_SIZE, TILES_ROW * TILE_SIZE),  pygame.RESIZABLE)

camera_group = CameraGroup()
player = Player((640,360), camera_group)

while True:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                pygame.quit()
                sys.exit()
            case pygame.WINDOWRESIZED:
                camera_group.custom_draw(player)
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            case pygame.MOUSEWHEEL:
                camera_group.zoom_scale += event.y * 0.03
    
    camera_group.update()
    camera_group.custom_draw(player)
    # screen.fill((0, 0, 0))
    
    pygame.display.update()
    clock.tick(60)