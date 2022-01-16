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
        self.max_lane_width = 70

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
        settings.selected_car.rect.x = self.width // 2 - settings.selected_car.rect.w // 2
        settings.vehicles = pygame.sprite.Group(settings.selected_car)

        # Render highways further
        self.preload_scroll = min(self.calc_textures_required(), 400)
        # print(self.preload_scroll)
        self.render_background()

    def render_background(self):
        settings.scroll.draw(self.screen)
        while len(settings.scroll) < self.preload_scroll:
            if len(settings.scroll) == 0:
                print('Reset occurred. Consider slowing down.')
                prev_y = self.height - settings.selected_highway.get_height()
            else:
                prev_y = min([s.rect.y for s in settings.scroll.sprites()])
            vh = self.create_highway_texture()
            if self.screen.get_width() > vh.get_total_lanes() * self.max_lane_width * settings.MSF:
                vh.set_texture(vh.get_texture(width=self.width - self.padding * 2))
            vh.rect.x = self.padding
            vh.rect.y = prev_y - settings.selected_highway.get_height()
        # print('Speed:', settings.selected_car.v, f'(about {(17.5/1600)*settings.selected_car.v*60*60/100000} kmph)')
        # print(len(settings.scroll))

    def render_cars(self):
        settings.vehicles.draw(self.screen)

    def prepare_car(self, car: resources.Vehicles.Vehicle.Vehicle):
        w = (self.width - self.padding * 2) / settings.selected_highway.get_total_lanes() * 0.6
        car.set_texture(car.get_texture(width=w))

    def prepare_highway(self, highway: resources.Highways.Highway.Highway):
        highway.set_texture(highway.get_texture(width=self.width))

    def calc_textures_required(self):
        h = settings.selected_highway.get_texture(width=self.width - self.padding * 2).get_rect().h
        if self.height // h < 10:
            return (self.height // h + 1) * 10
        elif self.height // h < 30:
            return (self.height // h + 1) * 5
        elif self.height // h < 50:
            return (self.height // h + 1) * 3
        else:
            return (self.height // h + 1) * 2

    def create_highway_texture(self):
        hw = settings.selected_highway
        nhw = resources.Highways.Highway.Highway(hw.name, hw.get_texture(), hw.lanes_per_direction, hw.two_directions)
        return nhw

    def move_highways(self):
        if len(settings.scroll.sprites()) <= 2:
            print('critically few HW')
            return 0
        for s in settings.scroll.sprites():
            s.rect.y += settings.selected_car.v

    def move_traffic(self):
        for sprite in settings.vehicles.sprites():
            if sprite.render and sprite != settings.selected_car and not sprite.crashed:
                if not sprite.reversed:
                    sprite.rect.y += settings.selected_car.v - settings.NPC_v
                else:
                    sprite.rect.y += settings.selected_car.v + settings.NPC_v
            elif sprite.render and sprite.crashed:
                sprite.rect.y += settings.selected_car.v
        
    # def darken_crash_animation(self):
        
    #     while t < 255:
            
    #         # surface.set_alpha(t)
            
    #         t += 5
    #         sleep(.01)


class AsyncRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.outputs = {}  # Follow structure {ThreadName: Data, ...}
        self.daemons = []
        self.run_daemons = True
        self.normal_daemons_count = 0
        self.last_car = None
        self.r = Renderer(screen)
        self.distance = 0

    def generate(self):
        # threading.Thread(target=self.move_traffic, daemon=True).start()
        # threading.Thread(target=self.move_highways, daemon=True).start()
        # threading.Thread(target=self.fill_scroll_new, daemon=True).start()
        threading.Thread(target=self.check_daemons, daemon=True).start()
        threading.Thread(target=self.remove_background_scroll, daemon=True).start()

    def create_daemons(self):
        self.daemons.append(threading.Thread(target=self.generate_new_cars, daemon=True))
        self.daemons.append(threading.Thread(target=self.remove_background_cars, daemon=True))
        # self.daemons.append(threading.Thread(target=self.fill_scroll, daemon=True).start())
        self.daemons.append(threading.Thread(target=self.remove_background_scroll, daemon=True))
        self.normal_daemons_count = len(self.daemons)
        for d in self.daemons:
            d.start()

    def generate_new_cars(self):
        while self.run_daemons:
            if self.last_car is None or self.last_car.rect.y > self.screen.get_height() / settings.level: 
                vhs = []
                for c in resources.Vehicles.Vehicle.create_all_vehicles(False):
                    if c.name != settings.selected_car.name:
                        vhs.append(c)
                vh = random.choice(vhs)
                self.r.prepare_car(vh)
                vh.rect.y = -200
                
                # Set lane
                num = random.randint(0, settings.selected_highway.get_total_lanes() - 1)
                vh.set_lane(num, width=settings.selected_highway.get_width())
                if settings.selected_highway.two_directions and num < settings.selected_highway.lanes_per_direction:
                    vh.reverse()
                vh.rect.x += settings.selected_highway.rect.x
                vh.do_render()
                self.last_car = vh
            sleep(settings.NPC_v / settings.selected_car.v)

    def remove_background_cars(self):
        res = 0
        while self.run_daemons:
            c = 0
            for car in settings.vehicles:
                # print(car.rect.y)
                try:
                    if car.rect.y > self.screen.get_height():
                        res += sys.getsizeof(car)
                        c += 1
                        car.kill()
                except AttributeError:
                    pass
            # print(f'Car GC: {c} removed, {len(settings.vehicles.sprites())} left. Lifetime stats: approx. {round(res / 1024 ** 2, 3)}MB cleared.')
            sleep(1)

    def remove_background_scroll(self):
        res = 0
        # while True:
        c = 0
        for hw in settings.scroll:
            if hw.rect.y > self.screen.get_height():
                res += sys.getsizeof(hw)
                c += 1
                hw.kill()
            # print(f'Highway GC: {c} removed, {len(settings.scroll.sprites())} left. Lifetime stats: approx. {round(res / 1024 ** 2, 3)}MB cleared.')
            # sleep(.1)

    # Deprecated, do NOT use
    def fill_scroll(self):
        while True:
            if len(settings.scroll) < 100:
                hw = self.r.create_highway_texture()
                hw.y = settings.scroll[0].y - hw.rect.h
                settings.scroll.insert(0, hw)
            # print(settings.scroll[0].y)
            # print('Count:', len(settings.scroll))
            sleep(.1)

    def stop(self):
        self.run_daemons = False
        for d in self.daemons:
            del d

    def check_daemons(self):
        if len(self.daemons) < self.normal_daemons_count:
            print('Error in daemon(s) occurred. Restarting...')
            self.stop
            sleep(0.001)
            self.create_daemons()
