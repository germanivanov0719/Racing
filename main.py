# Main libs imports
import pygame
import PyQt5

# Other libs imports
# EMPTY

# Other game parts
import resources.Highways.Highway
import gameplay.start_menu.welcome_window

# System constants
VERSION = "BASE-1"

# Game constants
# EMPTY

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption(f'Racing (version {VERSION})')
    size = width, height = 400, 400
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)

    running = True
    FPS = 60

    current_frame = 0  # to change speed of different elements

    gameplay.start_menu.welcome_window.generate_welcome()

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_frame = (current_frame + 1) % FPS
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()