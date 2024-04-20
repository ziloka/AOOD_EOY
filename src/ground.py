import json
import random
import pygame
from perlin_noise import PerlinNoise
from consts import *
from utils import *

class Ground(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.seed = random.randint(0, 100000)
        self.sprite_metadata = json.load(open("assets/metadata.json", "r"))
        self.noise = PerlinNoise(octaves=6, seed=self.seed)
        self.xpix, self.ypix = TILES_COLUMN, TILES_ROW
        self.tile_map = [[None] * self.xpix] * self.ypix
        self.generate_noisemap()
        self.generate_terrain()

    def move(self, screen_coordinates):
        self.generate_noisemap(screen_coordinates)
        self.generate_terrain()
        self.draw_terrain()

    def generate_noisemap(self, offset=[0, 0]):
        self.noise_map = [[self.noise([offset[0]+i/self.xpix, offset[1]+j/self.ypix]) for j in range(0, TILES_COLUMN)] for i in range(0, TILES_ROW)]

    def generate_terrain(self):
        for i in range(0, TILES_ROW):
            for j in range(0, TILES_COLUMN):
                column = self.noise_map[i][j]
                # https://stackoverflow.com/a/74592123
                for biome in biomes:
                    if column >= biome.value:
                        if self.tile_map[i][j] == None:
                            data = self.sprite_metadata[biome.name]
                            x = random.randint(0, data["columns"]-1) * TILE_SIZE
                            y = random.randint(0, data["rows"]-1) * TILE_SIZE
                            self.tile_map[i][j] = (x, y)

    def draw_terrain(self):
        for i in range(0, TILES_ROW):
            for j in range(0, TILES_COLUMN):
                column = self.noise_map[i][j]
                # https://stackoverflow.com/a/74592123
                for biome in biomes:
                    if column >= biome.value:
                        cropped = pygame.Surface((TILE_SIZE, TILE_SIZE))
                        cropped.blit(pygame.image.load(f"assets/{biome.name}.png"), (0, 0), (*self.tile_map[i][j], TILE_SIZE, TILE_SIZE))
                        cropped = pygame.transform.scale(cropped, (RESIZE_TILE, RESIZE_TILE))
                        self.screen.blit(cropped, (i * RESIZE_TILE, j * RESIZE_TILE))
