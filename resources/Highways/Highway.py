import pygame.image
import resources.Highways.Textures.TEXTURES
from resources.Highways.highway_generator import HighwayGeneration


def create_all_highways():
    # Change to get from DB
    textures = [resources.Highways.Textures.TEXTURES.ASPHALT_1,
                resources.Highways.Textures.TEXTURES.SNOW_1,
                resources.Highways.Textures.TEXTURES.DIRT_1]
    highways = []
    for t in textures:
        highways.append(resources.Highways.Highway.Highway(textures.index(t), t, 1, 1))
    return highways

# CREATE TABLE "highway_table" (
# 	"name"	INTEGER NOT NULL UNIQUE,
# 	"img"	TEXT NOT NULL,
# 	"lanes_per_direction"	TEXT NOT NULL,
# 	"two_directions"	INTEGER NOT NULL
# );

class Highway:
    def __init__(self, name, img, lanes_per_direction, two_directions=False):
        g = HighwayGeneration()
        self.img = g.generate(pygame.image.load(img), lanes_per_direction, two_directions)
        self.name = name
        self.size = self.img.get_rect().size

    def get_texture(self, scale=1):
        return pygame.transform.scale(self.img, (self.size[0] * scale // 1, self.size[1] * scale // 1))

    def get_width(self, scale=1):
        return self.size[0] * scale // 1

    def get_height(self, scale=1):
        return self.size[1] * scale // 1
