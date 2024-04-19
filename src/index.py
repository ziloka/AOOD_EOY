# py -m pip install perlin-noise pygame
import random
import pygame
import json
import sys
from pygame.locals import *
from perlin_noise import PerlinNoise
from consts import *
pygame.init()

clock = pygame.time.Clock()
sprite_metadata = json.load(open("assets/metadata.json", "r"))
screen = pygame.display.set_mode((TILES_COLUMN * TILE_SIZE, TILES_ROW * TILE_SIZE),  pygame.RESIZABLE)

# tile are resized to this size
RESIZE_TILE = 64
SEED = random.randint(0, 100000)

noise = PerlinNoise(octaves=6, seed=SEED)
xpix, ypix = TILES_COLUMN, TILES_ROW
noise_map = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
tile_map = [[0 for j in range(xpix)] for i in range(ypix)]

def draw_terrain():
    for i in range(0, TILES_ROW):
        for j in range(0, TILES_COLUMN):
            cropped = pygame.Surface((TILE_SIZE, TILE_SIZE))
            column = noise_map[i][j] # the smaller the number is the more likely it is going to show up
            # https://stackoverflow.com/a/74592123
            for biome in biomes:
                if column >= biome.value:
                    if tile_map[i][j] == 0:
                        data = sprite_metadata[biome.name]
                        x = random.randint(0, data["columns"]-1) * TILE_SIZE
                        y = random.randint(0, data["rows"]-1) * TILE_SIZE
                        tile_map[i][j] = (x, y)
                    cropped.blit(pygame.image.load(f"assets/{biome.name}.png"), (0, 0), (*tile_map[i][j], TILE_SIZE, TILE_SIZE))
                    cropped = pygame.transform.scale(cropped, (RESIZE_TILE, RESIZE_TILE))
                    screen.blit(cropped, (i * RESIZE_TILE, j * RESIZE_TILE))

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.WINDOWRESIZED:
            width, height = screen.get_width(), screen.get_height()

    draw_terrain()
    pygame.display.flip()
