from consts import *

# class Coordinates:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y

#     def screen_coords(self):
#         return self.x, self.y
    
#     def world_coords(self):
#         return self.x // TILE_SIZE, self.y // TILE_SIZE

def cords_convert_screen2world(x, y):
    return x // TILE_SIZE, y // TILE_SIZE