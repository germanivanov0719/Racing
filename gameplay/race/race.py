# Main libs imports
import pygame

# Other libs imports
import sys
import random

# Other game parts
import gameplay.start_menu.start_menu
import gameplay.highway_menu.highway_menu
from gameplay.settings_menu.settings import settings
import resources.Highways.Highway

# System constants
from main import VERSION

# Game constants
from resources.fonts.FONTS import ORBITRON_REGULAR, ORBITRON_MEDIUM, ORBITRON_EXTRA_BOLD


class Race:
    def __init__(self, heading_y=20):
        scaling = settings.get_scaling()
        # 1. Menu
        font = pygame.font.Font(ORBITRON_REGULAR, 20)
        self.menu = font.render('Menu', True, pygame.Color("green"))
        self.menu_x = self.menu.get_width()
        self.menu_y = self.menu.get_height()
        self.heading_y = heading_y  # For compatibility
        # General
        self.margin = 30

    def render(self, screen):
        # Menu button
        screen.blit(self.menu, (self.margin, self.margin + self.heading_y // 2 - self.menu_y // 2))
        pygame.draw.rect(screen, pygame.Color('green'),
                         (self.margin - 5, self.margin + self.heading_y // 2 - self.menu_y // 2 - 5,
                                                         self.menu_x + 10, self.menu_y + 10), 1)

    def click_handler(self, pos, screen):
        # Menu button
        rect = [range(self.margin - 5, self.margin - 5 + self.menu_x + 10),
                range(self.margin + self.heading_y // 2 - self.menu_y // 2 - 5, self.margin + self.heading_y // 2 - self.menu_y // 2 - 5 + self.menu_y + 10)]
        if pos[0] in rect[0] and pos[1] in rect[1]:
            new_menu = gameplay.highway_menu.highway_menu.HighwayMenu()
            return new_menu

        return self

    def right_click_handler(self, pos, screen):
        return self
        # new_menu = gameplay.start_menu.start_menu.StartMenu()
        # return new_menu
