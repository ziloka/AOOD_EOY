import math
import json
import random
import pygame
import numpy as np
from pygame.constants import *  
from perlin_noise import PerlinNoise
from consts import *
from utils import *
pygame.init()

font = pygame.font.SysFont(pygame.font.get_default_font(), 24)

class Tile():
    def __init__(self, num: int, biome: biomes):
        self.num = num
        self.biome = biome

class Ground(pygame.sprite.Group):
    def __init__(self, initial_offset=pygame.math.Vector2(0, 0)):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.ground = pygame.surface.Surface((self.screen.get_width(), self.screen.get_height()))
        self.seed = random.randint(0, 100000)
        self.sprite_metadata = json.load(open("assets/metadata.json", "r"))
        self.noise = PerlinNoise(octaves=8, seed=self.seed)

        self.sprites = {}
        for biome in biomes:
            self.sprites[biome.name] = []
            spritesheet = pygame.image.load(f"assets/{biome.name}.png").convert()
            for i in range(0, self.sprite_metadata[biome.name]["rows"]):
                for j in range(0, self.sprite_metadata[biome.name]["columns"]):
                    sprite = spritesheet.subsurface(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    resized_sprite = pygame.transform.scale(sprite, (RESIZE_TILE, RESIZE_TILE))
                    self.sprites[biome.name].append(resized_sprite)

        self.offset = initial_offset
        self.true_offset = pygame.math.Vector2(0, 0)
        self.delta_offset = pygame.math.Vector2(0, 0)

        self.calculate_tiles()
        self.generate_noisemap()
        self.generate_terrain()
        
    def calculate_tiles(self):
        self.xpix = math.ceil(self.screen.get_height() / RESIZE_TILE)
        self.ypix = math.ceil(self.screen.get_width() / RESIZE_TILE)

    def generate_noisemap(self, offset=pygame.math.Vector2(0, 0)):
        self.delta_offset += self.true_offset - offset
        self.true_offset = offset

        if not hasattr(self, "noise_map"):
            self.noise_map = np.arange(self.ypix * self.xpix, dtype=np.float16).reshape(self.ypix, self.xpix)
            for i in range(0, self.ypix):
                self.noise_map[i] = [self.noise([i/self.xpix, j/self.ypix]) for j in range(0, self.xpix)]
        # Determine what needs to be shifted and populate those values
        # https://stackoverflow.com/a/25628221
        elif self.delta_offset.x < RESIZE_TILE:
            self.noise_map = np.roll(self.noise_map, -2, axis=0)
            self.noise_map[:, 0] = [self.noise([(self.xpix + offset.x)/self.xpix, j/self.ypix]) for j in range(0, self.ypix)]
            # print(f"(player is going right) left shift self.xpix + offset.x = {self.xpix} + {offset.x}")
        elif self.delta_offset.x > RESIZE_TILE: 
            self.noise_map = np.roll(self.noise_map, 2, axis=0)
            self.noise_map[:, -1] = [self.noise([(self.xpix + offset.x)/self.xpix, j/self.ypix]) for j in range(0, self.ypix)]
            # print(f"(player is going left) right shift self.xpix + offset.x = {self.xpix} + {offset.x}")
        elif self.delta_offset.y < RESIZE_TILE: # down shift 
            self.noise_map = np.roll(self.noise_map, -1, axis=1)
            self.noise_map[-1] = [self.noise([i/self.xpix, (self.ypix + offset.y)/self.ypix]) for i in range(0, self.xpix)]
            # print(f"(player is going down) up shift self.ypix + offset.y = {self.ypix} + {offset.y}")
        elif self.delta_offset.y > RESIZE_TILE: # up shift
            self.noise_map = np.roll(self.noise_map, 1, axis=1)
            self.noise_map[0] = [self.noise([i/self.xpix, (self.ypix + offset.y)/self.ypix]) for i in range(0, self.xpix)]
            # print(f"(player is going up) down shift self.ypix + offset.y = {self.ypix} + {offset.y}")
        self.generate_terrain()

        if abs(self.delta_offset.x) > RESIZE_TILE:
            self.delta_offset.x = 0
        elif abs(self.delta_offset.y) > RESIZE_TILE:
            self.delta_offset.y = 0

    def generate_terrain(self):
        for i in range(0, self.ypix):
            for j in range(0, self.xpix):
                # https://stackoverflow.com/a/74592123
                for biome in biomes:
                    if self.noise_map[i][j] >= biome.value:
                        data = self.sprite_metadata[biome.name]
                        num = random.randint(0, data["columns"] * data["rows"])-1
                        self.ground.blit(self.sprites[biome.name][num], (i * RESIZE_TILE, j * RESIZE_TILE))
                        break

    def draw_terrain(self):
        pygame.display.get_surface().blit(self.ground, (0, 0))