# py -m pip install pillow numpy perlin-noise pygame

from PIL import Image
import numpy as np
from perlin_noise import PerlinNoise
import random
import pygame
import json
pygame.init()


# maximum 12 tiles in each row (keep 4:3 ratio)
TILES_HEIGHT = 24
TILES_WIDTH = 32

clock = pygame.time.Clock()

sprite_metadata = json.load(open("assets/metadata.json", "r"))

screen = pygame.display.set_mode((TILES_WIDTH * 16, TILES_HEIGHT * 16),  pygame.RESIZABLE)

noise = PerlinNoise(octaves=6, seed=random.randint(0, 100000))
xpix, ypix = screen.get_height(), screen.get_width()
pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]

while True:

  # limit fps
  clock.tick(60)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      run = False

  i = 0
  while i < screen.get_width():
    j = 0
    while j < screen.get_height():
      cropped = pygame.Surface((16, 16))
      print(i, j)
      column = pic[i][j]
      
  # for i, row in enumerate(pic):
  #   for j, column in enumerate(row):
  #     # if column>=0.6:
  #     #   screen.blit(pygame.image.load("assets/Tilled_Dirt.png"), (0, 0))
  #     # elif column >=-0.1:
  #     #   screen.blit(screen, (10, 210, 0), pygame.Rect(j, i, 1, 1))
      # if column >=-0.8:
      x = random.randint(0, 2) * 16 # 1 presenting the number of rows in dirt sprite - 1
      y = random.randint(0, 1) * 16
      # print(x, y)
      cropped.blit(pygame.image.load("assets/dirt.png"), (0, 0), (x, y, 16, 16))
      cropped = pygame.transform.scale(cropped, (16, 16))
      screen.blit(cropped, (i, j))
      j += 16
    i += 16
    pygame.display.flip()