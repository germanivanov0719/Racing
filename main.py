# Main libs imports
import pygame
import PyQt5

# System constants
VERSION = '0.1.2'

# Other libs imports
# EMPTY

# Other game parts
import gameplay.start_menu.welcome_window
import gameplay.start_menu.start_menu

# Game constants
# EMPTY


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption(f'Racing (version {VERSION})')
    size = width, height = 700, 700
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)

    running = True
    FPS = 60

    current_frame = 0  # to change speed of different elements

    gameplay.start_menu.welcome_window.generate_welcome()
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

        current_position.render(screen)
        current_frame = (current_frame + 1) % FPS
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


