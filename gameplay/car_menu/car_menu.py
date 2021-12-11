# Main libs imports
import pygame

# Other libs imports
import sys
import random

# Other game parts
import gameplay.start_menu.start_menu
import resources.Vehicles.Vehicle

# System constants
from main import VERSION

# Game constants
from resources.fonts.FONTS import COMIC_SANS_REGULAR, COMIC_SANS_BOLD, COMIC_SANS_ITALIC


class CarMenu:
    def __init__(self):
        # 1. Heading
        font = pygame.font.Font(COMIC_SANS_BOLD, 50)
        self.heading = font.render('Select Your Car', True, pygame.Color("yellow"))
        self.heading_x = self.heading.get_width()
        self.heading_y = self.heading.get_height()
        # Creating Vehicles
        self.textures = []
        textures = resources.Vehicles.Vehicle.create_all_vehicles()
        for t in textures:
            self.textures.append(resources.Vehicles.Vehicle.Vehicle(textures.index(t), t))
        self.selected = 1
        # Vehicle scroll
        self.margin = 30
        self.vertical_padding = 200
        self.scroll_height = 100
        self.edge_scale = 1.6
        self.selected_scale = 2
        # print(self.v)

    def render(self, screen):
        # Normal Elements
        screen.blit(self.heading, (screen.get_width() // 2 - self.heading_x // 2,
                                   20))
        # Arrows to select the vehicle
        pygame.draw.line(screen, pygame.Color('white'),
                         (self.margin // 3 * 2, self.vertical_padding + self.margin),
                         (self.margin // 3, self.vertical_padding + self.scroll_height // 2), 3)
        pygame.draw.line(screen, pygame.Color('white'),
                         (self.margin // 3, self.vertical_padding + self.scroll_height // 2),
                         (self.margin // 3 * 2, self.vertical_padding + self.scroll_height - self.margin), 3)

        pygame.draw.line(screen, pygame.Color('white'),
                         (screen.get_width() - self.margin // 3 * 2, self.vertical_padding + self.margin),
                         (screen.get_width() - self.margin // 3, self.vertical_padding + self.scroll_height // 2), 3)
        pygame.draw.line(screen, pygame.Color('white'),
                         (screen.get_width() - self.margin // 3, self.vertical_padding + self.scroll_height // 2),
                         (screen.get_width() - self.margin // 3 * 2, self.vertical_padding + self.scroll_height -
                          self.margin), 3)
        # Vehicles
        width = (screen.get_width() - self.margin * 4 - 2 * self.margin) // 3
        img_1 = self.textures[(self.selected - 1) % len(self.textures)]
        img_2 = self.textures[self.selected % len(self.textures)]
        img_3 = self.textures[(self.selected + 1) % len(self.textures)]

        screen.blit(img_1.get_texture(self.edge_scale),
                    (self.center_img_horizontally(self.margin, width, img_1.get_width(self.edge_scale), self.margin),
                     self.center_img_vertically(self.vertical_padding, self.scroll_height // 2, img_1.get_height(self.edge_scale))))
        screen.blit(img_2.get_texture(self.selected_scale),
                    (self.center_img_horizontally(2 * self.margin + width, width, img_2.get_width(self.selected_scale), self.margin),
                     self.center_img_vertically(self.vertical_padding, self.scroll_height // 2, img_2.get_height(self.selected_scale))))
        screen.blit(img_3.get_texture(self.edge_scale),
                    (self.center_img_horizontally(3 * self.margin + 2 * width, width, img_3.get_width(), self.margin),
                     self.center_img_vertically(self.vertical_padding, self.scroll_height // 2, img_3.get_height(self.edge_scale))))
        # Specifications and upgrades


    def click_handler(self, pos, screen):
        if pos[0] < screen.get_width() // 2:
            if self.selected - 1 < 0:
                self.selected = len(self.textures) - 1
            else:
                self.selected -= 1
        else:
            self.selected = (self.selected + 1) % len(self.textures)
        print(self.selected)
        return self

    def right_click_handler(self, pos, screen):
        new_menu = gameplay.start_menu.start_menu.StartMenu()
        return new_menu

    def center_img_horizontally(self, start, width, img_width, arrow_compensation=0):
        t = (width - img_width) // 2
        # print(t + start)
        return t + start + arrow_compensation

    def center_img_vertically(self, start, center, img_height):
        return start + center - img_height // 2