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
    def __init__(self, num, biome):
        self.num = num
        self.biome = biome

class Ground(pygame.sprite.Group):
    def __init__(self):
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

        self.calculate_tiles()
        self.generate_noisemap()
        self.generate_terrain()

        self.offset = pygame.math.Vector2(0, 0)

    def calculate_tiles(self):
        self.xpix = math.ceil(self.screen.get_height() / RESIZE_TILE)
        self.ypix = math.ceil(self.screen.get_width() / RESIZE_TILE)

    def move(self, screen_coordinates: pygame.math.Vector2):
        if abs(self.offset.x - screen_coordinates.x) > RESIZE_TILE or abs(self.offset.y - screen_coordinates.y) > RESIZE_TILE:
            self.generate_noisemap(screen_coordinates)
        self.generate_terrain()
        self.draw_terrain()

    def generate_noisemap(self, offset=pygame.math.Vector2(0, 0)):
        self.offset = offset
        num_shift_columns = math.ceil(offset.x / RESIZE_TILE)
        num_shift_rows = math.ceil(offset.y / RESIZE_TILE)

        # print(num_shift_columns, num_shift_rows)
        if not hasattr(self, "noise_map"):
            self.noise_map = np.arange(self.ypix * self.xpix, dtype=np.float16).reshape(self.ypix, self.xpix)
            for i in range(0, self.ypix):
                self.noise_map[i] = [self.noise([i/self.xpix, j/self.ypix]) for j in range(0, self.xpix)]
        elif num_shift_columns != 0 or num_shift_rows != 0:
            # Determine what needs to be shifted and populate those values
            # https://stackoverflow.com/a/25628221
            if num_shift_rows < 0: # shift columns to the right
                self.noise_map = np.roll(self.noise_map, num_shift_rows, axis=1)
                # print("before", self.noise_map[:, 0])
                self.noise_map[:, 0] = [self.noise([(self.xpix + offset.x)/self.xpix, j/self.ypix]) for j in range(0, self.ypix)]
                # print("right shift")
                # print("after", self.noise_map[:, 0])
            elif num_shift_rows > 0: # shift columns to the right
                self.noise_map = np.roll(self.noise_map, -num_shift_rows, axis=1)
                # print("before", self.noise_map[:, 0])
                # print("left shift")
                self.noise_map[:, -1] = [self.noise([(self.xpix + offset.x)/self.xpix, j/self.ypix]) for j in range(0, self.ypix)]
                # print("after", self.noise_map[:, 0])

            if num_shift_columns < 0: # shift rows down
                self.noise_map = np.roll(self.noise_map, num_shift_rows, axis=0)
                self.noise_map[0] = [self.noise([i/self.xpix, (self.ypix + offset.y)/self.ypix]) for i in range(0, self.xpix)]
                # print("down shift")
            elif num_shift_columns > 0: # shift rows up
                self.noise_map = np.roll(self.noise_map, -num_shift_rows, axis=0)
                self.noise_map[-1] = [self.noise([i/self.xpix, (self.ypix + offset.y)/self.ypix]) for i in range(0, self.xpix)]
                # print("up shift")

            self.generate_terrain()

            # if num_shift_columns > 0: # shift right
            #     self.noise_map = np.roll(self.noise_map, num_shift_columns, axis=1)
            #     self.noise_map[:, :num_shift_columns] = [self.noise([i/self.xpix, j/self.ypix]) for i in range(0, self.ypix) for j in range(0, num_shift_columns)]
            # elif num_shift_columns < 0: # shift left
            #     self.noise_map = np.roll(self.noise_map, -num_shift_columns, axis=1)
            #     self.noise_map[:, -num_shift_columns:] = [self.noise([i/self.xpix, j/self.ypix]) for i in range(0, self.ypix) for j in range(self.xpix + num_shift_columns, self.xpix)]

            # if num_shift_rows > 0: # shift down
            #     self.noise_map = np.roll(self.noise_map, num_shift_rows, axis=0)
            #     self.noise_map[:num_shift_rows, :] = [self.noise([i/self.xpix, j/self.ypix]) for i in range(0, num_shift_rows) for j in range(0, self.xpix)]
            # elif num_shift_rows < 0: # shift up
            #     self.noise_map = np.roll(self.noise_map, -num_shift_rows, axis=0)
            #     self.noise_map[-num_shift_rows:, :] = [self.noise([i/self.xpix, j/self.ypix]) for i in range(self.xpix + num_shift_rows, self.xpix)]

            # print("update array!")

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