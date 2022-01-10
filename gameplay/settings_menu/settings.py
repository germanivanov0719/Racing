import pygame.sprite

class Settings:
    def __init__(self):
        # Public
        self.VSYNC = True
        self.FPS = 60
        self.PRECISE_FPS = False
        self.CONTROLS = 'WASD'
        self.GSF = 1  # Global scaling factor, set by the user settings
        self.RSF = 1  # Resize (Real) scaling factor, calculated when the window is resized
        self.MSF = 1  # Minimal Scaling factor, calculated when the window is resized, used by Game Engine

        # Selected, public
        self.selected_car = None
        self.selected_highway = None
        self.vehicles = pygame.sprite.Group()
        self.NPC_v = 5
        self.scroll = pygame.sprite.Group()

        self.level = None
        
        # self.size = (900, 700)

        # Private
        self.__SCALING = 1  # Calculated as GSF * RSF

    def update_scaling(self):
        self.__SCALING = self.GSF * self.RSF

    def get_scaling(self) -> float:
        return self.__SCALING


settings = Settings()
