# Main libs imports
import pygame

# Other libs imports
import sys
import random

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
        # self.clock = pygame.

    def load_image(self, name):
        image = pygame.image.load(name)
        return image

    def render_background(self):
        # background = pygame.transform.scale(self.load_image('resources/Highways/Textures/road1.png'),
        #                                 (self.width, self.height))

        self.screen.blit(settings.selected_highway.get_texture(width=self.screen.get_width()), (0, 0))

    def render_player_car(self):
        # self.screen.blit(settings.selected_car.get_texture())
        settings.vehicles.draw(self.screen)
        # self.rect = self.play_car.get_rect().move(self.width // 2, self.height - self.height // 2.7)
        # TODO: draw car
