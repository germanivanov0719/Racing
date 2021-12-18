# Main libs imports
import pygame

# Other libs imports
# EMPTY

# Other game parts
import gameplay.car_menu.car_menu

# System constants
from main import VERSION

# Game constants
from resources.fonts.FONTS import COMIC_SANS_REGULAR, COMIC_SANS_BOLD, COMIC_SANS_ITALIC


class StartMenu:
    def __init__(self):
        # Defining the print
        # 1. Heading
        font = pygame.font.Font(COMIC_SANS_BOLD, 70)
        self.heading = font.render("Racing", True, pygame.Color("red"))
        self.heading_x = self.heading.get_width()
        self.heading_y = self.heading.get_height()
        # 2. Info
        font = pygame.font.Font(COMIC_SANS_REGULAR, 30)
        self.info = font.render(f"Version: {VERSION}", True, pygame.Color("red"))
        self.info_x = self.info.get_width()
        self.info_y = self.info.get_height()
        # 3. Play button
        font = pygame.font.Font(COMIC_SANS_BOLD, 65)
        self.play = font.render("Play", True, pygame.Color("green"))
        self.play_x = self.play.get_width()
        self.play_y = self.play.get_height()
        self.play_margin = 50

    def render(self, screen):
        screen.blit(self.heading, (screen.get_width() // 2 - self.heading_x // 2,
                                   screen.get_height() // 2 - self.heading_y // 2 - self.play_y))
        screen.blit(self.info, (10,
                                screen.get_height() - self.info_y))
        screen.blit(self.play, (screen.get_width() // 2 - self.play_x // 2,
                                screen.get_height() // 2 - self.play_y // 2 + self.play_margin))
        margin = self.play_margin // 2
        pygame.draw.rect(screen, pygame.Color('green'), (screen.get_width() // 2 - self.play_x // 2 - margin,
                                                         screen.get_height() // 2 - self.play_y // 2 + 2 * margin - 10,
                                                         self.play_x + 2 * margin,
                                                         self.play_y + margin), 3)

    def click_handler(self, pos, screen):
        margin = self.play_margin // 2
        rect = [range(screen.get_width() // 2 - self.play_x // 2 - margin,
                      screen.get_width() // 2 - self.play_x // 2 - margin + self.play_x + 2 * margin),
                range(screen.get_height() // 2 - self.play_y // 2 + 2 * margin - 10,
                      screen.get_height() // 2 - self.play_y // 2 + 2 * margin - 10 + self.play_y + margin)]
        if pos[0] in rect[0] and pos[1] in rect[1]:
            return gameplay.car_menu.car_menu.CarMenu()

    def right_click_handler(self, pos, screen):
        return self.click_handler(pos, screen)