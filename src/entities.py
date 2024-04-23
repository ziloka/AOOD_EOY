import math
import pygame
from ground import Ground
from consts import *

class Spritesheet:
    def __init__(self, filename, pos=(0, 0)):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.transcolor = self.sprite_sheet.get_at(pos)

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        sprite.set_colorkey(self.transcolor)
        return sprite

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(0, 0)

        self.ground = Ground()
        self.ground.draw_terrain()

    def center_target_camera(self, target):
        prevX, prevY = self.offset.x, self.offset.y
        self.offset.x = target.rect.centerx - self.display_surface.get_width() // 2
        self.offset.y = target.rect.centery - self.display_surface.get_height() // 2
        return prevX != self.offset.x or self.offset.y != prevY

    def custom_draw(self, player):
        changed = self.center_target_camera(player)

        ground_offset = self.offset
        if changed:
            self.ground.move(ground_offset)

        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

class Player(pygame.sprite.Sprite):
    DEFAULT_SIZE = (80, 120)
    ANI = 20
    def __init__(self, sprites, group):
        super().__init__(group)

        self.velx = 0
        self.vely = 0
        self.frame = 0

        self.images = []
        for sprite in sprites:
            img = pygame.transform.scale(sprite, Player.DEFAULT_SIZE)
            self.images.append(img)
        self.image = self.images[0]
        self.previmage = None

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velx
        self.rect.y += self.vely

        self.previmage = self.image
        if self.vely > 0:
            self.frame += 1 
            if self.frame >= 3*Player.ANI:
                self.frame = 0
            self.image = self.images[self.frame//Player.ANI]
        elif self.vely < 0:
            self.frame += 1 
            if self.frame >= 3*Player.ANI:
                self.frame = 0
            self.image = self.images[3 + self.frame//Player.ANI]
        elif self.velx < 0:
            self.frame += 1 
            if self.frame >= 3*Player.ANI:
                self.frame = 0
            self.image = self.images[6 + self.frame//Player.ANI]
        elif self.velx > 0:
            self.frame += 1 
            if self.frame >= 3*Player.ANI:
                self.frame = 0
            self.image = pygame.transform.flip(self.images[6 + self.frame//Player.ANI], True, False)
        else:
            try:
                ind = self.images.index(self.previmage)
            except ValueError:
                self.image = pygame.transform.flip(self.images[6], True, False)
                return
            if ind >= 6:
                self.image = self.images[6]
            elif ind >= 3:
                self.image = self.images[3]
            elif ind >= 0:
                self.image = self.images[0]
        
    #Setters
    def setVelX(self, velx):
        self.velx = velx
    def setVelY(self, vely):
        self.vely = vely

    #Getters    
    def getVelX(self):
        return self.velx
    def getVelY(self):
        return self.vely
    
class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load("Sprites/tree.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

class Slime(pygame.sprite.Sprite):
    DEFAULT_SIZE = (100, 100)
    def __init__(self, sprites, pos, player, group):
        super().__init__(group)

        self.ANI = 5

        self.animations = {
            "SPAWN": sprites[0],
            "IDLE": sprites[1],
            "MOVEL": sprites[2],
            "MOVER": sprites[3],
            "DEATH": sprites[0]
        }
        for state, arr in self.animations.items():
            l = []
            for sprite in arr:
                if state != "MOVER":
                    l.append(pygame.transform.scale(sprite, Slime.DEFAULT_SIZE))
                else:
                    l.append(pygame.transform.flip(pygame.transform.scale(sprite, Slime.DEFAULT_SIZE), True, False))
            self.animations[state] = l
        self.state = "SPAWN"

        self.velx = 0
        self.vely = 0
        self.frame = 0

        self.target = player

        self.images = self.animations[self.state]
        self.image = self.images[0]

        self.rect = self.image.get_rect(topleft=pos)
    
    def update(self):
        if math.sqrt((self.target.rect.x - self.rect.x) ** 2 + (self.target.rect.y - self.rect.y)**2) < 500:
            try:
                self.dir = pygame.Vector2(self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y).normalize() * 3
                self.velx = self.dir.x
                self.vely = self.dir.y 
            except Exception as e:
                print(f"Sqrt Error: {e}")
        else:
            self.velx = 0
            self.vely = 0

        self.rect.x += self.velx
        self.rect.y += self.vely

        if self.state == "IDLE" and self.velx != 0 or self.vely != 0:
            if self.velx < 0:
                self.state = "MOVEL"
            else:
                self.state = "MOVER"
            self.images = self.animations[self.state]
        elif (self.state == "MOVEL" or self.state == "MOVER") and self.velx == 0 and self.vely == 0:
            self.state = "IDLE"
            self.images = self.animations[self.state]

        if self.state == "SPAWN":
            self.frame += 1 
            if self.frame >= 16*self.ANI:
                self.frame = 0
                self.state = "IDLE"
                self.ANI = 10
                self.images = self.animations[self.state]
            self.image = self.images[self.frame//self.ANI]
        elif self.state == "IDLE":
            self.frame += 1 
            if self.frame >= 6*self.ANI:
                self.frame = 0
            self.image = self.images[self.frame//self.ANI]
        elif self.state == "MOVEL" or self.state == "MOVER":
            self.frame += 1 
            if self.frame >= 5*self.ANI:
                self.frame = 0
            self.image = self.images[self.frame//self.ANI]