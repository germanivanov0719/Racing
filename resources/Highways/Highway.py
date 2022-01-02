import sqlite3

import pygame.image
import resources.Highways.Textures.TEXTURES
from resources.Highways.highway_generator import HighwayGeneration
import os.path


def create_all_highways():
    # Change to get from DB
    db_path = os.path.join("resources/Highways/highways_table.db")
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    textures = [item[0] for item in cur.execute('SELECT img from highway_table').fetchall()]
    lanes_per_direction = [item[0] for item in cur.execute('SELECT lanes_per_direction from highway_table').fetchall()]
    two_directions = [item[0] for item in cur.execute('SELECT two_directions from highway_table').fetchall()]

    # textures = [resources.Highways.Textures.TEXTURES.ASPHALT_1,
    #             resources.Highways.Textures.TEXTURES.SNOW_1,
    #             resources.Highways.Textures.TEXTURES.DIRT_1]

    highways = []
    for car in range(len(textures)):
        highways.append(resources.Highways.Highway.Highway(car, textures[car], lanes_per_direction[car], two_directions[car]))

    # for t in textures:
    #     highways.append(resources.Highways.Highway.Highway(textures.index(t), t, 1, 1))
    return highways

# CREATE TABLE "highway_table" (
# 	"name"	TEXT NOT NULL UNIQUE,
# 	"img"	TEXT NOT NULL,
# 	"lanes_per_direction"	TEXT NOT NULL,
# 	"two_directions"	TEXT NOT NULL
# );

class Highway:
    def __init__(self, name, img, lanes_per_direction, two_directions=False):
        g = HighwayGeneration()
        self.__img = g.generate(pygame.image.load(img), lanes_per_direction, two_directions)
        self.name = name
        self.__size = self.__img.get_rect().size

    def get_texture(self, scale=1):
        return pygame.transform.scale(self.__img, (self.__size[0] * scale // 1, self.__size[1] * scale // 1))

    def get_width(self, scale=1):
        return self.__size[0] * scale // 1

    def get_height(self, scale=1):
        return self.__size[1] * scale // 1
