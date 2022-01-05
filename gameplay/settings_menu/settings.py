import pygame.sprite

class Settings:
    def __init__(self):
        # Public
        self.VSYNC = True
        self.FPS = 60
        self.PRECISE_FPS = False
        self.CONTROLS = 'WASD'
        self.GSF = 1  # Global scaling factor, set by the user settings
        self.RSF = 1  # Resize scaling factor, calculated when the window is resized

        # Selected, public
        self.selected_car = None
        self.selected_highway = None
        self.vehicles = pygame.sprite.Group()

        # Private
        self.__SCALING = 1  #

    def update_scaling(self):
        self.__SCALING = self.GSF * self.RSF

    def get_scaling(self) -> float:
        return self.__SCALING


settings = Settings()
