# Main libs imports
import pygame

# Other libs imports
import sys
import random

# Other game parts
import gameplay.start_menu.start_menu
import gameplay.highway_menu.highway_menu
from gameplay.settings_menu.settings import settings
import gameplay.race.renderer
import resources.Highways.Highway

# System constants
from main import VERSION

# Game constants
from resources.fonts.FONTS import ORBITRON_REGULAR, ORBITRON_MEDIUM, ORBITRON_EXTRA_BOLD


class Race:
    def __init__(self, heading_y=20):
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

    def render(self, screen):
        # Initialize renderer
        if self.r is None:
            self.r = gameplay.race.renderer.Renderer(screen)
        # Render GUI parts:
        # Prevent resizing
        if not self.screen_locked:
            screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), vsync=settings.VSYNC)
            self.screen_locked = True
        # Game engine:
        self.r.render_background()
        # Menu button
        screen.blit(self.menu, (self.margin, self.margin + self.heading_y // 2 - self.menu_y // 2))
        pygame.draw.rect(screen, pygame.Color('green'),
                         (self.margin - 5, self.margin + self.heading_y // 2 - self.menu_y // 2 - 5,
                          self.menu_x + 10, self.menu_y + 10), 1)

        # Render player car
        self.r.render_player_car()
        # Async
        ar = gameplay.race.renderer.AsyncRenderer()
        ar.move_traffic()

    def key_handler(self, screen, keys):
        # Use something like "if keys[pygame.K_w]:" to handle different keys.
        # Please, respect user preference, which is stored in "settings.CONTROLS"
        # and can be either 'WASD' or 'Arrows'.
        if keys[pygame.K_d]:
            settings.selected_car.rect.x += 9
            # if keys_down[pygame.K_w]:
            #     player.rect.
            # if keys_down[pygame.K_s]:
            #     velY = 10
        if keys[pygame.K_a]:
            settings.selected_car.rect.x -= 9
        if keys[pygame.K_w]:
            settings.selected_car.v += 1
        if keys[pygame.K_s]:
            settings.selected_car.v -= 1
            if settings.selected_car.v < settings.NPC_v + 2:
                #
                settings.selected_car.v = settings.NPC_v + 2
        # if keys[pygame.]
        pass

    def arrows_control(self, screen, keys):
        if keys[pygame.K_RIGHT]:
            settings.selected_car.rect.x += 9
        if keys[pygame.K_LEFT]:
            settings.selected_car.rect.x -= 9
        if keys[pygame.K_UP]:
            settings.selected_car.v += 1
        if keys[pygame.K_DOWN]:
            settings.selected_car.v -= 1
            if settings.selected_car.v < settings.NPC_v + 2:
                #
                settings.selected_car.v = settings.NPC_v + 2



    def click_handler(self, pos, screen):
        # Menu button
        rect = [range(self.margin - 5, self.margin - 5 + self.menu_x + 10),
                range(self.margin + self.heading_y // 2 - self.menu_y // 2 - 5,
                      self.margin + self.heading_y // 2 - self.menu_y // 2 - 5 + self.menu_y + 10)]
        if pos[0] in rect[0] and pos[1] in rect[1]:
            new_menu = gameplay.highway_menu.highway_menu.HighwayMenu()
            screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.RESIZABLE,
                                             vsync=settings.VSYNC)
            return new_menu

        return self

    def right_click_handler(self, pos, screen):
        return self
        # new_menu = gameplay.start_menu.start_menu.StartMenu()
        # return new_menu
