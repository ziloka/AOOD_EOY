# py -m pip install perlin-noise pygame
import sys
import random
import pygame
from pygame.locals import *

from consts import *
from entities import CameraGroup, Player, Spritesheet, Tree, Slime
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((TILES_COLUMN * TILE_SIZE, TILES_ROW * TILE_SIZE),  pygame.RESIZABLE)

camera_group = CameraGroup()

player_ss = Spritesheet('Sprites/PlayerSS.png')
player_sprites = [player_ss.get_sprite(15*j, 22*i, 14, 21) for j in range(3) for i in range(3)]

slime_ss = Spritesheet("Sprites/SlimeSS.png", (1, 1))
slime_sprites = []
slime_sprites.append([slime_ss.get_sprite(20 + 64*j, 692 + 61*i, 25, 25) for i in range(4) for j in range(5)])
slime_sprites.append([slime_ss.get_sprite(20 + 64*j, 364 + 63*i, 25, 25) for i in range(3) for j in range(3)])
slime_sprites.append([slime_ss.get_sprite(22 + 64*j, 556 + 63*i, 25, 25) for i in range(2) for j in range(3)])
slime_sprites.append([slime_ss.get_sprite(22 + 64*j, 556 + 63*i, 25, 25) for i in range(2) for j in range(3)])


#Trees
num_trees = 200
trees = []
while len(trees) <= num_trees:
    randomx = random.randint(-5000, 5000)
    randomy = random.randint(-5000, 5000)
    newtree = Tree((randomx, randomy), camera_group)
    for tree in trees:
        if newtree.rect.colliderect(tree.rect):
            newtree.kill()
    else:
        trees.append(newtree)


#Player
player = Player(player_sprites, camera_group)
player.rect.x = (screen.get_width() - player.rect.width)/2; player.rect.y = (screen.get_height() - player.rect.height)/2
player_spd  = 5 

#Slimes
num_slimes = 100
slimes = []
while len(slimes) <= num_slimes:
    randomx = random.randint(-5000, 5000)
    randomy = random.randint(-5000, 5000)
    newslime = Slime(slime_sprites, (randomx, randomy), player, camera_group)
    for slime in slimes:
        if newslime.rect.colliderect(slime.rect):
            newslime.kill()
    else:
        slimes.append(newslime)

while True:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                pygame.quit()
                sys.exit()
            case pygame.WINDOWRESIZED:
                camera_group.custom_draw(player)
                camera_group.ground.draw_terrain()
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
    clock.tick(60)