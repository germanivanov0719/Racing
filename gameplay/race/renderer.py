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
        self.y1 = -settings.selected_highway.get_height()
        self.y2 = 2 * self.y1
        self.back = settings.selected_highway.get_texture(width=self.width)
        self.scroll = [self.back, self.back, self.back]
        self.move = 0
        # self.clock = pygame.

    def load_image(self, name):
        image = pygame.image.load(name)
        return image

    def render_background(self):
        self.screen.blit(self.back, (0, self.move))
        for i in range(len(self. scroll)):
            if i == 0:
                self.screen.blit(self.scroll[i], (0, self.move))
            elif i == 1:
                self.screen.blit(self.scroll[i], (0, self.y1 + 5))
                self.y1 += 5
                self.move += 5
            else:
                self.screen.blit(self.scroll[i], (0, self.y2 + 5))
                self.y2 += 5
            if self.move == self.height:
                self.move = 0
                self.y1 = -settings.selected_highway.get_height()
                self.y2 = -settings.selected_highway.get_height() * 2











    def render_player_car(self):
        settings.vehicles.draw(self.screen)
        # settings.selected_car.check_collisions()
        # TODO: draw car

    # def update_background(self):




class AsyncRenderer:
    def move_traffic(self):
        for sprite in settings.vehicles:
            if sprite != settings.selected_car:
                sprite.rect.y += settings.selected_car.v - settings.NPC_v
