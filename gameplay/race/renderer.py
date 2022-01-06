# Main libs imports
import pygame

# Other libs imports
import sys
import random
import copy

# Other game parts
import gameplay.start_menu.start_menu
import gameplay.car_menu.car_menu
import resources.Highways.Highway
import gameplay.race.race
import resources.currency_operations
from gameplay.settings_menu.settings import settings


# System constants
from main import VERSION

# Game constants
from resources.fonts.FONTS import ORBITRON_REGULAR, ORBITRON_MEDIUM, ORBITRON_EXTRA_BOLD


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.background = settings.selected_highway
        self.preload_scroll = round(4 * settings.get_scaling())
        self.scroll = [copy.copy(self.background) for _ in range(self.preload_scroll)]
        for i in range(len(self.scroll) - 2):
            self.scroll[i].y = -self.background.get_height(width=self.width) * (len(self.scroll) - 2 - i)
        # self.scroll[0].y = -self.background.get_height(width=self.width)
        self.scroll[-1].y = self.background.get_height(width=self.width)

    def load_image(self, name):
        image = pygame.image.load(name)
        return image

    def render_background(self):
        for i in range(len(self.scroll)):
            self.screen.blit(self.scroll[i].get_texture(width=self.width), (0, self.scroll[i].y))
            self.scroll[i].y += settings.selected_car.v
            if self.scroll[i].y > self.height:
                del self.scroll[i]
                self.scroll.insert(0, copy.copy(self.background))
                self.scroll[0].y = -self.background.get_height(width=self.width)

    def render_player_car(self):
        settings.vehicles.draw(self.screen)


class AsyncRenderer:
    def move_traffic(self):
        for sprite in settings.vehicles:
            if sprite != settings.selected_car:
                sprite.rect.y += settings.selected_car.v - settings.NPC_v
