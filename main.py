# Main libs imports
import pygame
import PyQt5

# System constants
VERSION = '0.7'

# Other libs imports
# EMPTY

# Other game parts
import gameplay.start_menu.welcome_window
import gameplay.start_menu.start_menu
from gameplay.settings_menu.settings import settings
import gameplay.car_menu.car_menu
import gameplay.highway_menu.highway_menu
import gameplay.race.race

# Game constants
reinitialization_required = False
selected_highway = None
size = width, height = 900, 700  # Default size: 900x700, do not change these variables in code

if __name__ == '__main__':
    # Initializing the game
    pygame.init()

    # Setting system settings and variables
    pygame.display.set_caption(f'Racing (version {VERSION})')
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size, pygame.RESIZABLE, vsync=settings.VSYNC)
    running = True

    current_frame = 0  # to change speed of different elements

    # Start a game with the welcome window
    gameplay.start_menu.welcome_window.generate_welcome()

    # Initialize the 1st menu
    current_position = gameplay.start_menu.start_menu.StartMenu()

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    r = current_position.click_handler(pos=event.pos, screen=screen)
                    if r is not None:
                        current_position = r
                if event.button == pygame.BUTTON_RIGHT:
                    r = current_position.right_click_handler(pos=event.pos, screen=screen)
                    if r is not None:
                        current_position = r
            # Check if window is resized
            if event.type == pygame.VIDEORESIZE:
                w = screen.get_width()
                h = screen.get_height()
                # Check if size is too small
                if w < width / 3:
                    w = width // 3
                if h < height / 3:
                    h = height // 3
                if (w, h) != (screen.get_width(), screen.get_height()):
                    screen = pygame.display.set_mode((w, h), pygame.RESIZABLE, vsync=settings.VSYNC)

                # Some magical calculations to make the screen look as beautiful as possible
                settings.RSF = abs(sorted([w / width - 1, h / height - 1])[0] + 1)
                settings.MSF = abs(sorted([w / width - 1, h / height - 1])[1] + 1)
                # Applying scaling
                settings.update_scaling()
                del w, h
                if type(current_position) in [gameplay.car_menu.car_menu.CarMenu, gameplay.highway_menu.highway_menu.HighwayMenu]:
                    sel = current_position.selected
                    current_position.__init__(selected=sel)
                else:
                    current_position.__init__()

        if type(current_position) == gameplay.race.race.Race:
            current_position.key_handler(screen, keys=pygame.key.get_pressed())

        current_position.render(screen)
        current_frame = (current_frame + 1) % settings.FPS
        pygame.display.flip()
        if settings.PRECISE_FPS:
            clock.tick_busy_loop(settings.FPS)
        else:
            clock.tick(settings.FPS)

    pygame.quit()
