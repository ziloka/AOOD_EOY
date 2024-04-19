# py -m pip install perlin-noise pygame
import random
import pygame
import json
from pygame.locals import *
from perlin_noise import PerlinNoise
from consts import *
pygame.init()

clock = pygame.time.Clock()
sprite_metadata = json.load(open("assets/metadata.json", "r"))
screen = pygame.display.set_mode((TILES_COLUMN * TILE_SIZE, TILES_ROW * TILE_SIZE),  pygame.RESIZABLE)

# tile are resized to this size
RESIZE_TILE = 64

noise = PerlinNoise(octaves=6, seed=random.randint(0, 100000))
xpix, ypix = TILES_COLUMN, TILES_ROW
pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
print(f"pic: # rows: {len(pic)}, # cols: {len(pic[0])}")
print(f"RESIZE TILE: {RESIZE_TILE}")

def draw_terrain():
  for i in range(0, TILES_ROW):
    for j in range(0, TILES_COLUMN):
      cropped = pygame.Surface((TILE_SIZE, TILE_SIZE))
      column = pic[i][j]
      
      x = random.randint(0, 2) * TILE_SIZE # 1 presenting the number of rows in dirt sprite - 1
      y = random.randint(0, 1) * TILE_SIZE
      # print(x, y)
      cropped.blit(pygame.image.load("assets/dirt.png"), (0, 0), (x, y, TILE_SIZE, TILE_SIZE))
      cropped = pygame.transform.scale(cropped, (RESIZE_TILE, RESIZE_TILE))
      screen.blit(cropped, (i * RESIZE_TILE, j * RESIZE_TILE))

while True:
  clock.tick(60)  # limit fps
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
    if event.type == pygame.WINDOWRESIZED:
      width, height = screen.get_width(), screen.get_height()

  draw_terrain()
  pygame.display.flip()
