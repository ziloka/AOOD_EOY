from enum import Enum

# maximum 12 tiles in each row (keep 4:3 ratio)
TILES_COLUMN = 32
TILES_ROW = 24

# in each spritesheet, sprites are 16 by 16
TILE_SIZE = 16

# the smaller the number is the more likely it is going to show up
class biomes(Enum):
    dirt = -0.8
    grass = 0.002