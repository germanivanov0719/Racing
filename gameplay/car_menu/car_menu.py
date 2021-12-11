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
        # 2. Back
        font = pygame.font.Font(COMIC_SANS_REGULAR, 24)
        self.back = font.render('Back', True, pygame.Color("green"))
        self.back_x = self.back.get_width()
        self.back_y = self.back.get_height()
        # Creating Vehicles
        self.vehicles = resources.Vehicles.Vehicle.create_all_vehicles()
        self.selected = 1
        # Vehicle scroll
        self.margin = 30
        self.vertical_padding = 200
        self.scroll_height = 100
        self.edge_scale = 1.6
        self.selected_scale = 2
        # print(self.v)

    def render(self, screen):
        # Heading
        screen.blit(self.heading, (screen.get_width() // 2 - self.heading_x // 2,
                                   20))
        # Back button
        screen.blit(self.back, (self.margin, self.margin))
        pygame.draw.rect(screen, pygame.Color('green'), (self.margin - 5, self.margin - 5,
                                                         self.back_x + 10, self.back_y + 10), 1)
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
        img_1 = self.vehicles[(self.selected - 1) % len(self.vehicles)]
        img_2 = self.vehicles[self.selected % len(self.vehicles)]
        img_3 = self.vehicles[(self.selected + 1) % len(self.vehicles)]

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
        # Back button
        (self.margin - 5, self.margin - 5,
         self.back_x + 10, self.back_y + 10)
        rect = [range(self.margin - 5, self.margin - 5 + self.back_x + 10),
                range(self.margin - 5, self.margin - 5 + self.back_y + 10)]
        if pos[0] in rect[0] and pos[1] in rect[1]:
            new_menu = gameplay.start_menu.start_menu.StartMenu()
            return new_menu
        if pos[0] < screen.get_width() // 2:
            if self.selected - 1 < 0:
                self.selected = len(self.vehicles) - 1
            else:
                self.selected -= 1
        else:
            self.selected = (self.selected + 1) % len(self.vehicles)
        print(self.selected)
        return self

    def right_click_handler(self, pos, screen):
        return self
        # new_menu = gameplay.start_menu.start_menu.StartMenu()
        # return new_menu

    def center_img_horizontally(self, start, width, img_width, arrow_compensation=0):
        t = (width - img_width) // 2
        # print(t + start)
        return t + start + arrow_compensation

    def center_img_vertically(self, start, center, img_height):
        return start + center - img_height // 2
