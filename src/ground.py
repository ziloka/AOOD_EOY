import math
import json
import random
import pygame
from perlin_noise import PerlinNoise
from consts import *

class Tile():
    def __init__(self, x, y, biome):
        self.x = x
        self.y = y
        self.biome = biome

class Ground(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.seed = random.randint(0, 100000)
        self.sprite_metadata = json.load(open("assets/metadata.json", "r"))
        self.sprites = {biomes.name: pygame.image.load(f"assets/{biomes.name}.png") for biomes in biomes}
        self.noise = PerlinNoise(octaves=8, seed=self.seed)
        self.calculate_tiles()
        self.generate_noisemap()
        self.generate_terrain()

    def calculate_tiles(self):
        self.xpix = math.ceil(self.screen.get_height() / RESIZE_TILE)
        self.ypix = math.ceil(self.screen.get_width() / RESIZE_TILE)
        self.tile_map = [[None] * self.xpix] * self.ypix

    def move(self, screen_coordinates):
        self.generate_noisemap(screen_coordinates)
        self.generate_terrain()
        self.draw_terrain()

    def generate_noisemap(self, offset=[0, 0]):
        self.noise_map = [[self.noise([offset[0]+i/self.xpix, offset[1]+j/self.ypix]) for j in range(0, self.xpix)] for i in range(0, self.ypix)]

    def generate_terrain(self):
        for i in range(0, self.ypix):
            for j in range(0, self.xpix):
                # print(self.ypix, self.xpix, i, j)
                column = self.noise_map[i][j]
                # https://stackoverflow.com/a/74592123
                for biome in biomes:
                    if column >= biome.value:
                        print(column, biome.name, biome.value)
                        data = self.sprite_metadata[biome.name]
                        x = random.randint(0, data["columns"]-1) * TILE_SIZE
                        y = random.randint(0, data["rows"]-1) * TILE_SIZE
                        self.tile_map[i][j] = Tile(x, y, biome)
                        break

    def draw_terrain(self):
        for i in range(0, self.ypix):
            for j in range(0, self.xpix):
                tile = self.tile_map[i][j]
                # column = self.noise_map[i][j]
                # https://stackoverflow.com/a/74592123
                # for biome in biomes:
                #     if column >= biome.value:
                        # print(tile.biome.name, biome.name)
                cropped = pygame.Surface((TILE_SIZE, TILE_SIZE))
                cropped.blit(self.sprites[tile.biome.name], (0, 0), (tile.x, tile.y, TILE_SIZE, TILE_SIZE))
                cropped = pygame.transform.scale(cropped, (RESIZE_TILE, RESIZE_TILE))
                self.screen.blit(cropped, (i * RESIZE_TILE, j * RESIZE_TILE))
