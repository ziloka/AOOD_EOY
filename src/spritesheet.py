import pygame
import json

SPRITESHEETMAP = "Tutorial Project-04_04_2024.json"

# Sprite Sheet Class:
class SpriteSheet(object):

    def __init__(self,loc,file) -> None:
        
        self.__loc__ = loc
        self.__file__ = file
        self.__title__ = ''
        self.__sprite_sheet__ = ''
        self.__animation_speed__ = 0
        self.__dims__ = (0,0)
        self.__keys__ = list()
        self.__suffkeys__ = list()
        self.__vmlines__ = dict()
        self.__subby__ = dict()
        self.__init_map__()
        self.__sprite_sheet_image__ = self.__init_spritesheet_image()
        self.__sprites__ = self.__generate_sprites__()
    
    def __init_spritesheet_image(self) -> pygame.Surface:
        return pygame.image.load(self.__loc__+self.sprite_sheet()).convert_alpha()
    
    def __init_map__(self):

        # Init Variable setup:
        ssmap = self.read_spritesheet_map(self.__loc__+self.__file__)
        ssmapd = json.load(ssmap).get(SPRITESHEETMAP)

        # Operate on JSON file properties:
        self.title(ssmapd.get(TITLE))
        self.sprite_sheet(ssmapd.get(SPRITE_SHEET))
        self.animation_speed(ssmapd.get(ANIMATION_SPEED))
        self.dimensions(ssmapd.get(DIMS))
        self.keys(ssmapd.get(KEYS))
        self.suffkeys(ssmapd.get(SUFF_KEYS))

        self.valuemap_lines(ssmapd.get(VALUES_MAP))
        for x in self.valuemap_lines():
            self.__subby__[x]=SpriteDetails.new(self.valuemap_lines()[x].get(SPRITE_DETAILS))
        
    def __generate_sprites__(self):
        ret = dict()
        for k in self.__subby__:
            ta = list()
            sd = self.__subby__[k]
            r = sd.row()
            c = sd.count()
            s = sd.start()
            i = 0
            while i < c:
                tup = (
                    (s)+(self.dimensions()[0]*i),
                    (self.dimensions()[1]*r)
                )+self.dimensions()
                ta.append(
                    self.__sprite_sheet_image__.subsurface(tup)
                )
                i += 1
            ret[k]=ta
        return ret

    def sprites(self) -> dict:
        return self.__sprites__
    def title(self,s=None) -> str:
        if s != None:
            self.__title__ = s
        return self.__title__
    def sprite_sheet(self,s=None) -> str:
        if s != None:
            self.__sprite_sheet__ = s
        return self.__sprite_sheet__
    def animation_speed(self,s=None) -> float:
        if s != None:
            self.__animation_speed__ = s
        return self.__animation_speed__
    def dimensions(self,s=None) -> tuple:
        if s != None:
            self.__dims__ = s
        return tuple(self.__dims__)
    def keys(self,s=None) -> list:
        if s != None:
            self.__keys__ = s
        return self.__keys__
    def suffkeys(self,s=None) -> list:
        if s != None:
            self.__suffkeys__ = s
        return self.__suffkeys__
    def valuemap_lines(self,s=None) -> dict:
        if s != None:
            self.__vmlines__ = s
        return self.__vmlines__
    def read_spritesheet_map(self,file):
        f = io.FileIO(file,'r+')
        return f