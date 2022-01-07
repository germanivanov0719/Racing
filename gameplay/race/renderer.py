# Main libs imports
from time import sleep

import pygame

# Other libs imports
import sys
import random
import copy
import threading
import random

# Other game parts
import gameplay.start_menu.start_menu
import gameplay.car_menu.car_menu
import resources.Highways.Highway
import gameplay.race.race
import resources.Vehicles.Vehicle
import resources.currency_operations
from gameplay.settings_menu.settings import settings


# System constants
from main import VERSION
import main

# Game constants
from resources.fonts.FONTS import ORBITRON_REGULAR, ORBITRON_MEDIUM, ORBITRON_EXTRA_BOLD

scroll = []

class Renderer:
    def __init__(self, screen):
        global scroll
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.prepare_car(settings.selected_car)
        settings.selected_car.rect.y = int(self.height * .8 - settings.selected_car.rect[3])
        settings.selected_car.rect.x = self.width // 2 - settings.selected_car.rect.x // 2
        settings.vehicles = pygame.sprite.Group(settings.selected_car)

        self.preload_scroll = round(4 * settings.get_scaling())
        self.scroll = [copy.copy(settings.selected_highway) for _ in range(self.preload_scroll)]
        for i in range(len(self.scroll) - 2):
            self.scroll[i].y = -settings.selected_highway.get_height(width=self.width) * (len(self.scroll) - 2 - i)
        self.scroll[-1].y = settings.selected_highway.get_height(width=self.width)

    # def move_highways(self):
    #     global scroll
    #     for i in scroll:
    #         i.y += settings.selected_car.v

    def render_background(self):
        for i in range(len(self.scroll)):
            self.screen.blit(self.scroll[i].get_texture(width=self.width), (0, self.scroll[i].y))
            self.scroll[i].y += settings.selected_car.v
            if self.scroll[i].y > self.height:
                del self.scroll[i]
                self.scroll.insert(0, copy.copy(settings.selected_highway))
                self.scroll[0].y = -settings.selected_highway.get_height(width=self.width)

    def render_cars(self):
        settings.vehicles.draw(self.screen)

    def prepare_car(self, car: resources.Vehicles.Vehicle.Vehicle):
        w = self.width / settings.selected_highway.get_total_lanes() * 0.6
        car.set_texture(car.get_texture(width=w))

    # def prepare_highway(self, highway: resources.Highways.Highway.Highway):
    #     highway.set_texture(highway.get_texture(width=self.width))

    def calc_textures_required(self):
        h = settings.selected_highway.get_texture(width=self.width).get_rect()[3]
        return self.height // h + 5

    def create_highway_texture(self):
        hw = settings.selected_highway
        nhw = resources.Highways.Highway.Highway(hw.name, hw.get_texture(), hw.lanes_per_direction, hw.two_directions)
        return nhw


class AsyncRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.outputs = {}  # Follow structure {ThreadName: Data, ...}
        self.daemons = []
        self.last_car = None
        self.r = Renderer(screen)

    def generate(self):
        threading.Thread(target=self.move_traffic, daemon=True).start()
        # threading.Thread(target=self.move_highways, daemon=True).start()

    def create_daemons(self):
        self.daemons.append(threading.Thread(target=self.generate_new_cars, daemon=True).start())
        self.daemons.append(threading.Thread(target=self.remove_background_cars, daemon=True).start())
        self.daemons.append(threading.Thread(target=self.fill_scroll, daemon=True).start())
        self.daemons.append(threading.Thread(target=self.remove_background_scroll, daemon=True).start())

    def move_traffic(self):
        for sprite in settings.vehicles:
            if sprite != settings.selected_car and sprite.render:
                sprite.rect.y += settings.selected_car.v - settings.NPC_v

    def generate_new_cars(self):
        while True:
            if self.last_car is None or self.last_car.rect.y > self.last_car.rect[3] + 50:
                num = random.randint(0, settings.selected_highway.get_total_lanes() - 1)
                vhs = resources.Vehicles.Vehicle.create_all_vehicles(False)
                vh = vhs[random.randint(0, len(vhs) - 1)]
                self.r.prepare_car(vh)
                vh.rect.y = -200
                vh.set_lane(num, width=self.screen.get_width())
                vh.do_render()
                self.last_car = vh
            sleep(settings.NPC_v / settings.selected_car.v)

    def remove_background_cars(self):
        while True:
            for car in settings.vehicles:
                if car.rect.y > self.screen.get_height() * 2:
                    del car
            sleep(10)

    def remove_background_scroll(self):
        global scroll
        while True:
            c = 0
            for hw in scroll:
                if hw.y > self.screen.get_height():
                    del hw
                    c += 1
            # print('Removed:', str(c), 'Remaining:', str(len(scroll)))
            sleep(.1)
            
    def fill_scroll(self):
        while True:
            global scroll
            if len(scroll) < 10:
                # if scroll[1].y > 0:
                #     settings.selected_car.v = settings.NPC_v
                #     del scroll
                #     scroll = [self.r.create_highway_texture() for _ in range(self.r.calc_textures_required())]
                #     for i in range(len(scroll) - 2):
                #         scroll[i].y = -scroll[0].get_height(width=self.width) * (len(scroll) - 2 - i)
                #     for i in scroll:
                #         self.r.prepare_highway(i)
                #     scroll[-1].y = scroll[0].get_height(width=self.width)
                hw = self.r.create_highway_texture()
                hw.y = scroll[0].y
                scroll.insert(0, hw)
                # scroll[0].y = -scroll[1].y * len(scroll) - 2
            print(scroll[0].y)

                # scroll.append(self.r.create_highway_texture())
                # scroll.append(self.r.create_highway_texture())
                #
                # print(scroll[0].get_height(width=self.screen.get_width()), scroll[0].get_width(), self.screen.get_width())
                # scroll[1].y = -(len(scroll) - 3) * scroll[0].get_height(width=self.screen.get_width())
                # # scroll[0].y = -100
                # # scroll[1].y = -200
                # print(scroll[0].y, scroll[1].y)
            print('Count:', len(scroll))
                # sleep(0.0001)
            sleep(.1)
