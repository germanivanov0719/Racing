# Important note:
# All non-playable vehicles must have size ≥ player vehicle's size
import pygame.image
import resources.Vehicles.Textures.TEXTURES
import sqlite3
import os


def create_all_vehicles():
    db_path = os.path.join("resources/Vehicles/vehicles_table.db")
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    textures = [item[0] for item in cur.execute('SELECT img from vehicle_table').fetchall()]
    speed = [item[0] for item in cur.execute('SELECT speed from vehicle_table').fetchall()]
    brakes = [item[0] for item in cur.execute('SELECT brakes from vehicle_table').fetchall()]
    acceleration = [item[0] for item in cur.execute('SELECT acceleration from vehicle_table').fetchall()]
    speed_multiplier = [item[0] for item in cur.execute('SELECT speed_multiplier from vehicle_table').fetchall()]
    brakes_multiplier = [item[0] for item in cur.execute('SELECT brakes_multiplier from vehicle_table').fetchall()]
    acceleration_multiplier = [item[0] for item in cur.execute('SELECT acceleration_multiplier from vehicle_table').fetchall()]

    # textures = [resources.Vehicles.Textures.TEXTURES.BUS_1,
    #             resources.Vehicles.Textures.TEXTURES.BUS_2,
    #             resources.Vehicles.Textures.TEXTURES.BUS_3,
    #             resources.Vehicles.Textures.TEXTURES.BUS_4,
    #             resources.Vehicles.Textures.TEXTURES.BUS_5]

    vehicles = []
    for car in range(len(textures)):
        vehicles.append(resources.Vehicles.Vehicle.Vehicle(car, textures[car], speed[car], brakes[car], acceleration[car]))
    return vehicles

    # for t in textures:
    #     vehicles.append(resources.Vehicles.Vehicle.Vehicle(textures.index(t), t, 1, 1, 1))


# CREATE TABLE "vehicle_table" (
# 	"name"	TEXT NOT NULL UNIQUE,
# 	"img"	TEXT NOT NULL,
# 	"speed"	INTEGER NOT NULL,
# 	"brakes"	INTEGER NOT NULL,
# 	"acceleration"	INTEGER NOT NULL,
# 	"speed_multiplier"	INTEGER NOT NULL,
# 	"brakes_multiplier"	INTEGER NOT NULL,
# 	"acceleration_multiplier"	INTEGER NOT NULL
# );


class Vehicle:
    def __init__(self, name, img, speed, brakes, acceleration, multipliers=(1, 1, 1)):
        self.__img = pygame.image.load(img)
        self.name = name
        self.__size = self.__img.get_rect().size

        self.speed_multiplier = multipliers[0]
        self.brakes_multiplier = multipliers[1]
        self.acceleration_multiplier = multipliers[2]

        # Change to data from the Car DB
        self.speed = speed
        self.brakes = brakes
        self.acceleration = acceleration

    def get_texture(self, scale=1):
        return pygame.transform.scale(self.__img, (self.__size[0] * scale // 1, self.__size[1] * scale // 1))

    def get_width(self, scale=1):
        return self.__size[0] * scale // 1

    def get_height(self, scale=1):
        return self.__size[1] * scale // 1
