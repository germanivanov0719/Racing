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
import gameplay

# System constants
from main import VERSION

# Game constants
from resources.fonts.FONTS import ORBITRON_REGULAR, ORBITRON_MEDIUM, ORBITRON_EXTRA_BOLD


class HighwayMenu:
    def __init__(self):
        # 1. Heading
        font = pygame.font.Font(ORBITRON_MEDIUM, 50)
        self.heading = font.render('Select a Highway', True, pygame.Color("yellow"))
        self.heading_x = self.heading.get_width()
        self.heading_y = self.heading.get_height()
        # 2. Back
        font = pygame.font.Font(ORBITRON_REGULAR, 20)
        self.back = font.render('Back', True, pygame.Color("green"))
        self.back_x = self.back.get_width()
        self.back_y = self.back.get_height()
        # 3. Play
        font = pygame.font.Font(ORBITRON_REGULAR, 30)
        self.Play = font.render('Play', True, pygame.Color("green"))
        self.Play_x = self.Play.get_width()
        self.Play_y = self.Play.get_height()
        self.arrow_margin_down = 10
        self.arrow_height = 20
        self.arrow_margin = 20
        # Creating Vehicles
        self.highways = resources.Highways.Highway.create_all_highways()
        self.selected = 1
        # General
        self.margin = 30
        # Vehicle scroll
        self.vertical_padding = 200
        self.scroll_height = 100
        self.edge_scale = .8
        self.selected_scale = 1.15
        # print(self.v)

    def render(self, screen):
        # Heading
        screen.blit(self.heading, (screen.get_width() // 2 - self.heading_x // 2,
                                   self.margin))
        # Back button
        screen.blit(self.back, (self.margin, self.margin + self.heading_y // 2 - self.back_y // 2))
        pygame.draw.rect(screen, pygame.Color('green'),
                         (self.margin - 5, self.margin + self.heading_y // 2 - self.back_y // 2 - 5,
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
        img_1 = self.highways[(self.selected - 1) % len(self.highways)]
        img_2 = self.highways[self.selected % len(self.highways)]
        img_3 = self.highways[(self.selected + 1) % len(self.highways)]

        screen.blit(img_1.get_texture(self.edge_scale),
                    (self.center_img_horizontally(self.margin, width, img_1.get_width(self.edge_scale), self.margin),
                     self.center_img_vertically(self.vertical_padding, self.scroll_height // 2, img_1.get_height(self.edge_scale))))
        screen.blit(img_2.get_texture(self.selected_scale),
                    (self.center_img_horizontally(2 * self.margin + width, width, img_2.get_width(self.selected_scale), self.margin),
                     self.center_img_vertically(self.vertical_padding, self.scroll_height // 2, img_2.get_height(self.selected_scale))))
        screen.blit(img_3.get_texture(self.edge_scale),
                    (self.center_img_horizontally(3 * self.margin + 2 * width, width, img_3.get_width(), self.margin),
                     self.center_img_vertically(self.vertical_padding, self.scroll_height // 2, img_3.get_height(self.edge_scale))))
        # Weather and Difficulty

        # Play button
        screen.blit(self.Play, (screen.get_width() - self.Play_x - self.margin,
                                screen.get_height() - self.Play_y - self.margin))
        pygame.draw.line(screen, pygame.Color("green"),
                         (screen.get_width() - self.Play_x - self.margin + self.arrow_margin, screen.get_height() - self.Play_y - self.arrow_margin_down - self.margin),
                         (screen.get_width() - self.margin - self.arrow_margin, screen.get_height() - self.Play_y - self.arrow_margin_down - self.arrow_height - self.margin), 8)
        pygame.draw.line(screen, pygame.Color("green"),
                         (screen.get_width() - self.margin - self.arrow_margin,
                          screen.get_height() - self.Play_y - self.arrow_margin_down - self.arrow_height - self.margin),
                         (screen.get_width() - self.Play_x - self.margin + self.arrow_margin,
                          screen.get_height() - self.Play_y - self.arrow_margin_down - 2 * self.arrow_height - self.margin),
                         8)

    def click_handler(self, pos, screen):
        # Back button
        rect = [range(self.margin - 5, self.margin - 5 + self.back_x + 10),
                range(self.margin + self.heading_y // 2 - self.back_y // 2 - 5, self.margin + self.heading_y // 2 - self.back_y // 2 - 5 + self.back_y + 10)]
        if pos[0] in rect[0] and pos[1] in rect[1]:
            new_menu = gameplay.car_menu.car_menu.CarMenu()
            return new_menu

        # Play button
        if pos[0] > screen.get_width() - 150 and pos[1] > screen.get_height() - 150:
            return gameplay.race.race.Race(heading_y=self.heading_y)

        # Scroll buttons
        if pos[0] < (screen.get_width() - 150) // 2 and pos[1] in range(self.vertical_padding, self.vertical_padding + self.scroll_height):
            if self.selected - 1 < 0:
                self.selected = len(self.highways) - 1
            else:
                self.selected -= 1
        if pos[0] > (screen.get_width() + 150) // 2 and pos[1] in range(self.vertical_padding, self.vertical_padding + self.scroll_height):
            self.selected = (self.selected + 1) % len(self.highways)

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