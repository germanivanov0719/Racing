# Important note:
# All non-playable vehicles must have size ≥ player vehicle's size
import pygame.image
import resources.Vehicles.Textures.TEXTURES
import sqlite3
import pygame.sprite
from gameplay.settings_menu.settings import settings


def create_all_vehicles():
    con = sqlite3.connect('resources/Vehicles/vehicles_table.db')
    cur = con.cursor()
    names = [item[0] for item in cur.execute('SELECT name from vehicle_table').fetchall()]
    textures = [item[0] for item in cur.execute('SELECT img from vehicle_table').fetchall()]
    speed = [item[0] for item in cur.execute('SELECT speed from vehicle_table').fetchall()]
    brakes = [item[0] for item in cur.execute('SELECT brakes from vehicle_table').fetchall()]
    acceleration = [item[0] for item in cur.execute('SELECT acceleration from vehicle_table').fetchall()]
    speed_multipliers = [item[0] for item in cur.execute('SELECT speed_multiplier from vehicle_table').fetchall()]
    brakes_multipliers = [item[0] for item in cur.execute('SELECT brakes_multiplier from vehicle_table').fetchall()]
    acceleration_multipliers = [item[0] for item in cur.execute('SELECT acceleration_multiplier from vehicle_table').fetchall()]
    cur.close()

    # textures = [resources.Vehicles.Textures.TEXTURES.BUS_1,
    #             resources.Vehicles.Textures.TEXTURES.BUS_2,
    #             resources.Vehicles.Textures.TEXTURES.BUS_3,
    #             resources.Vehicles.Textures.TEXTURES.BUS_4,
    #             resources.Vehicles.Textures.TEXTURES.BUS_5]

    vehicles = []
    for car in range(len(names)):
        vehicles.append(resources.Vehicles.Vehicle.Vehicle(names[car], textures[car], speed[car], brakes[car], acceleration[car], (speed_multipliers[car], brakes_multipliers[car], acceleration_multipliers[car])))
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
# 	"acceleration_multiplier"	INTEGER NOT NULL,
# 	"cost"	INTEGER
# );


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, name, img, speed, brakes, acceleration, multipliers=(1, 1, 1), x=0, y=0):
        super().__init__(settings.vehicles)
        self.image = pygame.image.load(img)
        self.name = name
        self.__size = self.image.get_rect().size

        self.speed = speed
        self.brakes = brakes
        self.acceleration = acceleration

        self.speed_multiplier = multipliers[0]
        self.brakes_multiplier = multipliers[1]
        self.acceleration_multiplier = multipliers[2]

        self.x, self.y = x, y
        self.rect = self.image.get_rect()

    def get_texture(self, scale=1):
        return pygame.transform.scale(self.image, (self.__size[0] * scale // 1, self.__size[1] * scale // 1))

    def get_width(self, scale=1):
        return self.__size[0] * scale // 1

    def get_height(self, scale=1):
        return self.__size[1] * scale // 1

    def get_multipliers(self):
        return self.speed_multiplier, self.brakes_multiplier, self.acceleration_multiplier

    def set_speed_multiplier(self, new_speed_multiplier):
        con = sqlite3.connect('resources/Vehicles/vehicles_table.db')
        cur = con.cursor()
        cur.execute(f"UPDATE vehicle_table SET speed_multiplier = {new_speed_multiplier} WHERE name = '{self.name}'")
        con.commit()
        con.close()

    def set_brakes_multiplier(self, new_brakes_multiplier):
        con = sqlite3.connect('resources/Vehicles/vehicles_table.db')
        cur = con.cursor()
        cur.execute(f"UPDATE vehicle_table SET brakes_multiplier = {new_brakes_multiplier} WHERE name = '{self.name}'")
        con.commit()
        con.close()

    def set_acceleration_multiplier(self, new_acceleration_multiplier):
        con = sqlite3.connect('resources/Vehicles/vehicles_table.db')
        cur = con.cursor()
        cur.execute(f"UPDATE vehicle_table SET acceleration_multiplier = {new_acceleration_multiplier} WHERE name = '{self.name}'")
        con.commit()
        con.close()
