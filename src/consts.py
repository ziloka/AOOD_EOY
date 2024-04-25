from enum import Enum

# in each spritesheet, sprites are 16 by 16
TILE_SIZE = 16

# tile are resized to this size
RESIZE_TILE = 64

# the smaller the number is the more likely it is going to show up
class biomes(Enum):
    grass = 0.5
    dirt = 0.4
