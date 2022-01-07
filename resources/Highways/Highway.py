import sqlite3

import pygame.image
import resources.Highways.Textures.TEXTURES
from resources.Highways.highway_generator import HighwayGeneration
from gameplay.settings_menu.settings import settings


def create_all_highways():
    # Change to get from DB
    con = sqlite3.connect('resources/Highways/highways_table.db')
    cur = con.cursor()
    names = [item[0] for item in cur.execute('SELECT name from highway_table').fetchall()]
    textures = [item[0] for item in cur.execute('SELECT img from highway_table').fetchall()]
    lanes_per_direction = [item[0] for item in cur.execute('SELECT lanes_per_direction from highway_table').fetchall()]
    two_directions = [item[0] for item in cur.execute('SELECT two_directions from highway_table').fetchall()]

    # textures = [resources.Highways.Textures.TEXTURES.ASPHALT_1,
    #             resources.Highways.Textures.TEXTURES.SNOW_1,
    #             resources.Highways.Textures.TEXTURES.DIRT_1]

    highways = []
    for car in range(len(textures)):
        highways.append(resources.Highways.Highway.Highway(names[car], textures[car], lanes_per_direction[car], two_directions[car]))

    # for t in textures:
    #     highways.append(resources.Highways.Highway.Highway(textures.index(t), t, 1, 1))
    return highways

# CREATE TABLE "highway_table" (
# 	"name"	TEXT NOT NULL UNIQUE,
# 	"img"	TEXT NOT NULL,
# 	"lanes_per_direction"	INTEGER,
# 	"two_directions"	INTEGER NOT NULL DEFAULT 0,
# 	"cost"	INTEGER
# );


class Highway(pygame.sprite.Sprite):
    def __init__(self, name, img, lanes_per_direction, two_directions=False):
        super().__init__(settings.scroll)
        if isinstance(img, pygame.Surface):
            self.image = img
        else:
            self.image = pygame.image.load(img)
        self.name = name
        self.rect = self.image.get_rect()
        self.lanes_per_direction = lanes_per_direction
        self.two_directions = two_directions
        # self.x, self.y = 0, 0

    def get_texture(self, scale=1, width=None, height=None):
        if width is not None:
            scale = width / self.rect.w
        if height is not None:
            scale = height / self.rect.h
        if width is not None and height is not None:
            return pygame.transform.scale(self.image, (width, height))
        return pygame.transform.scale(self.image, (self.rect[2] * scale // 1, self.rect[3] * scale // 1))

    def set_texture(self, surface: pygame.Surface):
        self.image = surface
        self.rect = surface.get_rect()

    def get_width(self, scale=1, width=None, height=None):
        if width is not None:
            return int(self.rect.w * (height / self.rect.h))
        return self.rect.w * scale // 1

    def get_height(self, scale=1, width=None, height=None):
        if width is not None:
            return int(self.rect.h * (width / self.rect.w))
        return self.rect.h * scale // 1

    def get_total_lanes(self) -> int:
        return self.lanes_per_direction * (self.two_directions + 1)

    def get_size(self):
        return self.rect
