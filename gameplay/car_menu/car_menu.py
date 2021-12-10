# Main libs imports
import pygame

# Other libs imports
import sys
import random

# Other game parts
import gameplay.start_menu.start_menu

# System constants
from main import VERSION

# Game constants
from resources.fonts.FONTS import COMIC_SANS_REGULAR, COMIC_SANS_BOLD, COMIC_SANS_ITALIC


class CarMenu:
    def __init__(self):
        self.hash = random.randint(1, 1000000000)
        font = pygame.font.Font(COMIC_SANS_BOLD, 65)
        self.h = font.render(str(self.hash), True, pygame.Color("green"))
        self.h_x = self.h.get_width()
        self.h_y = self.h.get_height()

    def render(self, screen):
        screen.blit(self.h, (screen.get_width() // 2 - self.h_x // 2,
                             screen.get_height() // 2 - self.h_y // 2))

    def click_handler(self, pos, screen):
        return self

    def right_click_handler(self, pos, screen):
        new_menu = gameplay.start_menu.start_menu.StartMenu()
        return new_menu

