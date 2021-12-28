# Important note:
# All non-playable vehicles must have size ≥ player vehicle's size
import pygame.image
import resources.Vehicles.Textures.TEXTURES


def create_all_vehicles():
    # Change to get from DB
    textures = [resources.Vehicles.Textures.TEXTURES.BUS_1,
                resources.Vehicles.Textures.TEXTURES.BUS_2,
                resources.Vehicles.Textures.TEXTURES.BUS_3,
                resources.Vehicles.Textures.TEXTURES.BUS_4,
                resources.Vehicles.Textures.TEXTURES.BUS_5]
    vehicles = []
    for t in textures:
        vehicles.append(resources.Vehicles.Vehicle.Vehicle(textures.index(t), t, 1, 1, 1))
    return vehicles


class Vehicle:
    def __init__(self, name, img, speed, brakes, acceleration, multipliers=(1, 1, 1)):
        self.img = pygame.image.load(img)
        self.name = name
        self.size = self.img.get_rect().size

        self.speed_multiplier = multipliers[0]
        self.brakes_multiplier = multipliers[1]
        self.acceleration_multiplier = multipliers[2]

        # Change to data from the Car DB
        self.speed = speed
        self.brakes = brakes
        self.acceleration = acceleration

    def get_texture(self, scale=1):
        return pygame.transform.scale(self.img, (self.size[0] * scale // 1, self.size[1] * scale // 1))

    def get_width(self, scale=1):
        return self.size[0] * scale // 1

    def get_height(self, scale=1):
        return self.size[1] * scale // 1
