# https://github.com/clear-code-projects/Tiled/blob/eacaf2ae129bdd029009770770d40e963c229a12/code/tiled_code.py
# py -m pip install pillow pygame
# JSON file is exported from https://spritefusion.com

import sys
import io
import json
import base64
import pygame
from PIL import Image

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,surf,groups):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
data = json.loads(open('../assets/Tutorial Project-08_04_2024.json', "r").read())
# https://stackoverflow.com/a/32517907
surfaces = {}

# https://stackoverflow.com/a/75501713
# https://www.geeksforgeeks.org/how-to-convert-pil-image-into-pygame-surface-image/
for key, dataURL in data["spriteSheets"].items():
	scheme, base64URL = dataURL.split(",")
	bytes = base64.b64decode(base64URL)
	im = Image.open(io.BytesIO(bytes))
	surfaces[key] = pygame.image.frombytes(im.tobytes(), im.size, im.mode)

sprite_group = pygame.sprite.Group()

for (i, layer) in enumerate(data["layers"]):
	print(f"Layer {i+1}: {layer['name']}")
	for tile in layer["tiles"]:
		x, y, spriteSheetId, scaleX = tile["x"], tile["y"], tile["spriteSheetId"], tile["scaleX"]
		surf = surfaces[spriteSheetId]
		pos = (x, y)
		Tile(pos = pos, surf = surf, groups = sprite_group)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.fill('black')
	sprite_group.draw(screen)
	
	pygame.display.update()