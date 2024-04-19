import json
import random
import pygame
from perlin_noise import PerlinNoise
from consts import *

class Terrain(pygame.sprite.Group):
    def __init__(self, seed):
        super.__init__(self)
        self.sprite_metadata = json.load(open("assets/metadata.json", "r"))

        self.noise = PerlinNoise(octaves=6, seed=seed)
        self.xpix, self.ypix = TILES_COLUMN, TILES_ROW
        self.noise_map = [[self.noise([i/self.xpix, j/self.ypix]) for j in range(self.xpix)] for i in range(self.ypix)]
        self.tile_map = [[None] * self.xpix] * self.ypix
        self.entities = []
        self.self.systems = []

    def move(self, x, y):
        print("moved x, y")
        pass

    def draw_terrain(self):
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
                        cropped = pygame.Surface((TILE_SIZE, TILE_SIZE))
                        cropped.blit(pygame.image.load(f"assets/{biome.name}.png"), (0, 0), (*self.tile_map[i][j], TILE_SIZE, TILE_SIZE))
                        cropped = pygame.transform.scale(cropped, (RESIZE_TILE, RESIZE_TILE))
                        screen.blit(cropped, (i * RESIZE_TILE, j * RESIZE_TILE))

    def add_entity(self, entity):
        self.entities.append(entity)

    def add_system(self, system):
        self.systems.append(system)

    def update(self):
        for system in self.systems:
            system.update(self.entities)