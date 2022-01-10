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


class Renderer:
    def __init__(self, screen):
        # Initializing, setting general variables
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        # Setting up highways, and drawing the first one
        self.max_lane_width = 100

        settings.scroll = pygame.sprite.Group(settings.selected_highway)
        hw = settings.selected_highway
        self.padding = 0
        if hw.get_total_lanes() * self.max_lane_width * settings.MSF < self.width:
            width = hw.get_total_lanes() * self.max_lane_width * settings.MSF
            self.padding = (self.width - width) // 2
            hw.set_texture(hw.get_texture(width=width))
        else:
            hw.set_texture(hw.get_texture(width=self.width))
        hw.rect.x = self.padding
        hw.rect.y = self.height - hw.get_height()

        # Setting up the player's car
        self.prepare_car(settings.selected_car)
        settings.selected_car.rect.y = int(self.height * .8 - settings.selected_car.rect.h)
        settings.selected_car.rect.x = self.width // 2 - settings.selected_car.rect.x // 2
        settings.vehicles = pygame.sprite.Group(settings.selected_car)

        # Render highways further
        self.preload_scroll = round(50 * settings.get_scaling())
        self.render_background()

    def render_background(self):
        settings.scroll.draw(self.screen)
        print(settings.selected_car.v)
        while len(settings.scroll) < self.preload_scroll:
            if len(settings.scroll) == 0:
                prev_y = 0
            else:
                prev_y = min([s.rect.y for s in settings.scroll.sprites()])
            vh = self.create_highway_texture()
            if self.screen.get_width() > vh.get_total_lanes() * self.max_lane_width * settings.MSF:
                # width = vh.get_total_lanes() * self.max_lane_width * settings.get_scaling()
                vh.set_texture(vh.get_texture(width=self.width - self.padding * 2))
                vh.rect.y = prev_y - settings.selected_highway.get_height()
                vh.rect.x = self.padding
            else:
                vh.rect.y = prev_y - settings.selected_highway.get_height(width=self.screen.get_width())

    def render_cars(self):
        settings.vehicles.draw(self.screen)

    def prepare_car(self, car: resources.Vehicles.Vehicle.Vehicle):
        w = (self.width - self.padding * 2) / settings.selected_highway.get_total_lanes() * 0.6
        car.set_texture(car.get_texture(width=int(w)))

    def prepare_highway(self, highway: resources.Highways.Highway.Highway):
        highway.set_texture(highway.get_texture(width=self.width))

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
        self.distance = 0
        # self.car_remove_distance = /

    def generate(self):
        threading.Thread(target=self.move_traffic, daemon=True).start()
        threading.Thread(target=self.move_highways, daemon=True).start()

    def create_daemons(self):
        self.daemons.append(threading.Thread(target=self.generate_new_cars, daemon=True).start())
        self.daemons.append(threading.Thread(target=self.remove_background_cars, daemon=True).start())
        # self.daemons.append(threading.Thread(target=self.fill_scroll, daemon=True).start())
        self.daemons.append(threading.Thread(target=self.remove_background_scroll, daemon=True).start())

    def move_traffic(self):
        for sprite in settings.vehicles:
            if sprite != settings.selected_car and sprite.render:
                sprite.rect.y += settings.selected_car.v - settings.NPC_v

    def generate_new_cars(self):
        while True:
            if self.last_car is None or self.last_car.rect.y > self.screen.get_height():
                num = random.randint(0, settings.selected_highway.get_total_lanes() - 1)
                vhs = []
                for c in resources.Vehicles.Vehicle.create_all_vehicles(False):
                    if c.name != settings.selected_car.name:
                        vhs.append(c)
                vh = random.choice(vhs)
                self.r.prepare_car(vh)
                vh.rect.y = -200
                vh.set_lane(num, width=settings.selected_highway.get_width())
                vh.rect.x += settings.selected_highway.rect.x
                vh.do_render()
                self.last_car = vh
            sleep(settings.NPC_v / settings.selected_car.v)

    def remove_background_cars(self):
        res = 0
        while True:
            c = 0
            for car in settings.vehicles:
                # print(car.rect.y)
                if car.rect.y > self.screen.get_height():
                    res += sys.getsizeof(car)
                    c += 1
                    car.kill()
            # print(f'Car GC: {c} removed, {len(settings.vehicles.sprites())} left. Lifetime stats: approx. {round(res / 1024 ** 2, 3)}MB cleared.')
            sleep(1)

    def remove_background_scroll(self):
        res = 0
        while True:
            c = 0
            for hw in settings.scroll:
                if hw.rect.y > self.screen.get_height():
                    res += sys.getsizeof(hw)
                    c += 1
                    hw.kill()
            # print(f'Highway GC: {c} removed, {len(settings.scroll.sprites())} left. Lifetime stats: approx. {round(res / 1024 ** 2, 3)}MB cleared.')
            sleep(.1)

    def fill_scroll(self):
        while True:
            if len(settings.scroll) < 100:
                hw = self.r.create_highway_texture()
                hw.y = settings.scroll[0].y - hw.rect.h
                settings.scroll.insert(0, hw)
            print(settings.scroll[0].y)
            print('Count:', len(settings.scroll))
            sleep(.1)

    def move_highways(self):
        for s in settings.scroll.sprites():
            s.rect.y += settings.selected_car.v
