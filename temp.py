# py -m pip install pillow numpy perlin-noise pygame

from PIL import Image
import numpy as np
from perlin_noise import PerlinNoise
import random
import pygame
import json
pygame.init()

noise = PerlinNoise(octaves=6, seed=random.randint(0, 100000))
xpix, ypix = 500, 500
pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]

sprite_metadata = json.load(open("assets/metadata.json", "r"))

screen = pygame.display.set_mode((500, 500),  pygame.RESIZABLE)

for i in range(0, screen.get_height()):
  j = 0
  while j <= screen.get_width():
    cropped = pygame.Surface((16, 16))
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
    print(x, y)
    cropped.blit(pygame.image.load("assets/dirt.png"), (0, 0), (x, y, 16, 16))
    pygame.transform.scale(cropped, (256, 256))
    screen.blit(cropped, (i, j))
    j += 16
  i += 16


while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      run = False

        # pygame.draw.rect(screen, (0, 0, 200), pygame.Rect(j, i, 1, 1))
  pygame.display.flip()

