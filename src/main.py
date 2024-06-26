import cProfile
import sys
import random
import pygame
from entities import *
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
fps = 60

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = window.get_size()
pygame.display.set_caption('AOOD EOY Game')

#Camera
camera_group = CameraGroup()

player_ss = Spritesheet('assets/PlayerSS.png')
player_sprites = [player_ss.get_sprite(15*j, 22*i, 14, 21) for j in range(3) for i in range(3)]

player = Player(player_sprites, camera_group)
player.rect.x = (WIDTH - player.rect.width)/2; player.rect.y = (HEIGHT - player.rect.height)/2
player_spd  = 5 

slime_ss = Spritesheet("assets/SlimeSS.png", (1, 1))
slime_sprites = []
slime_sprites.append([slime_ss.get_sprite(20 + 64*j, 692 + 61*i, 25, 25) for i in range(4) for j in range(5)])
slime_sprites.append([slime_ss.get_sprite(20 + 64*j, 364 + 63*i, 25, 25) for i in range(3) for j in range(3)])
slime_sprites.append([slime_ss.get_sprite(22 + 64*j, 556 + 63*i, 25, 25) for i in range(2) for j in range(3)])
slime_sprites.append([slime_ss.get_sprite(22 + 64*j, 556 + 63*i, 25, 25) for i in range(2) for j in range(3)])

num_trees = 200
trees: list[Tree] = []
while len(trees) <= num_trees:
    randomx = random.randint(-5000, 5000)
    randomy = random.randint(-5000, 5000)
    newtree = Tree((randomx, randomy), camera_group)
    for tree in trees:
        if newtree.rect.colliderect(tree.rect):
            newtree.kill()
    else:
        trees.append(newtree)

num_slimes = 10
slimes: list[Slime] = []
while len(slimes) <= num_slimes:
    randomx = random.randint(-5000, 5000)
    randomy = random.randint(-5000, 5000)
    newslime = Slime(slime_sprites, (randomx, randomy), player, camera_group)
    for slime in slimes:
        if newslime.rect.colliderect(slime.rect):
            newslime.kill()
    else:
        slimes.append(newslime)

font = pygame.font.SysFont(pygame.font.get_default_font(), 24)

#Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.setVelX(-player_spd)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.setVelX(player_spd)
            if event.key == pygame.K_UP or event.key == ord('w'):
                player.setVelY(-player_spd)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                player.setVelY(player_spd)
        elif event.type == pygame.KEYUP:
            if player.getVelX() < 0 and (event.key == pygame.K_LEFT or event.key == ord('a')):
                player.setVelX(0)
            if player.getVelX() > 0 and (event.key == pygame.K_RIGHT or event.key == ord('d')):
                player.setVelX(0)
            if player.getVelY() < 0 and (event.key == pygame.K_UP or event.key == ord('w')):
                player.setVelY(0)
            if player.getVelY() > 0 and (event.key == pygame.K_DOWN or event.key == ord('s')):
                player.setVelY(0) 
            if event.key == ord('q') or event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    window.fill((255, 255, 255))

    camera_group.custom_draw(player)
    camera_group.update()

    text_surface = font.render(str(clock.get_fps()), False, (0, 0, 0))
    window.blit(text_surface, (0, 0))

    pygame.display.update()
    clock.tick(fps)
