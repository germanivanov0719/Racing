# Main libs imports
import threading
import time

import pygame

# Other libs imports
import sys
import random

# Other game parts
import gameplay.start_menu.start_menu
import gameplay.highway_menu.highway_menu
from gameplay.settings_menu.settings import settings
import gameplay.race.renderer
import resources.currency_operations
from gameplay.race.reset_on_exit import reset
import resources.Highways.Highway

# System constants
from main import VERSION

# Game constants
from resources.fonts.FONTS import ORBITRON_REGULAR, ORBITRON_MEDIUM, ORBITRON_EXTRA_BOLD


class Race:
    def __init__(self, heading_y=20):
        settings.update_scaling()
        scaling = settings.get_scaling()
        # 1. Menu
        font = pygame.font.Font(ORBITRON_REGULAR, int(20 * scaling))
        self.menu = font.render('Menu', True, pygame.Color("green"))
        self.menu_x = self.menu.get_width()
        self.menu_y = self.menu.get_height()
        self.heading_y = heading_y  # For compatibility
        # General
        self.margin = int(30 * scaling)
        # Prevent resizing
        self.screen_locked = False
        # Create renderer instance
        self.r = None
        self.ar = None
        # Count distance
        self.distance = 0

    def render(self, screen):
        # Initialize renderer and async renderer
        if self.r is None or self.ar is None:
            self.r = gameplay.race.renderer.Renderer(screen)
            self.ar = gameplay.race.renderer.AsyncRenderer(screen)
            self.ar.create_daemons()

        # Prevent resizing
        if not self.screen_locked:
            screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), vsync=settings.VSYNC)
            self.screen_locked = True

        # Call all threads to make them start performing background tasks before rendering
        self.ar.generate()

        # Game engine:
        # Highways
        self.r.render_background()
        self.r.move_highways()
        # Cars
        self.r.render_cars()
        self.r.move_traffic()

        # Render GUI parts (must always be at the top):
        # Menu button
        screen.blit(self.menu, (self.margin, self.margin + self.heading_y // 2 - self.menu_y // 2))
        pygame.draw.rect(screen, pygame.Color('green'),
                         (self.margin - 5, self.margin + self.heading_y // 2 - self.menu_y // 2 - 5,
                          self.menu_x + 10, self.menu_y + 10), 1)

        # Check player collisions
        if pygame.sprite.spritecollide(settings.selected_car, settings.vehicles, False) != [settings.selected_car]:
            settings.selected_car.kill()

        self.distance += settings.selected_car.v
        # print(self.distance)

    def key_handler(self, screen, keys):
        # Use something like "if keys[pygame.K_w]:" to handle different keys.
        # Please, respect user preference, which is stored in "settings.CONTROLS"
        # and can be either 'WASD' or 'Arrows'.
        car = settings.selected_car
        arrows_on = settings.CONTROLS == 'Arrows'
        if arrows_on and keys[pygame.K_RIGHT] or not arrows_on and keys[pygame.K_d]:
            car.rect.x += 6 / (settings.FPS / 60)
        if arrows_on and keys[pygame.K_LEFT] or not arrows_on and keys[pygame.K_a]:
            car.rect.x -= 6 / (settings.FPS / 60)
        if arrows_on and keys[pygame.K_UP] or not arrows_on and keys[pygame.K_w]:
            car.v += car.get_acceleration() / (settings.FPS / 60)
            if settings.selected_car.v > settings.selected_car.get_speed():
                settings.selected_car.v = settings.selected_car.get_speed()
        if arrows_on and keys[pygame.K_DOWN] or not arrows_on and keys[pygame.K_s]:
            car.v -= car.get_brakes() / (settings.FPS / 60)
            if car.v < settings.NPC_v + 2:
                car.v = settings.NPC_v + 2

    def click_handler(self, pos, screen):
        # Menu button
        rect = [range(self.margin - 5, self.margin - 5 + self.menu_x + 10),
                range(self.margin + self.heading_y // 2 - self.menu_y // 2 - 5,
                      self.margin + self.heading_y // 2 - self.menu_y // 2 - 5 + self.menu_y + 10)]
        if pos[0] in rect[0] and pos[1] in rect[1]:
            # Make screen resizable again
            screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.RESIZABLE,
                                             vsync=settings.VSYNC)
            # Give the player money for the ride
            # Level multipliers: 100, 125, 150%
            m = self.distance / 2500 * (1 + (settings.level - 1) * .25)
            # TODO: Call a Qt dialog later
            co = resources.currency_operations.CurrencyOperations()
            co.add(int(m))

            self.ar.stop()
            del self.r
            time.sleep(.001)
            del self.ar

            reset()  # Call to reinitialize all objects
            return gameplay.highway_menu.highway_menu.HighwayMenu()

        return self

    def right_click_handler(self, pos, screen):
        return self
        # new_menu = gameplay.start_menu.start_menu.StartMenu()
        # return new_menu
