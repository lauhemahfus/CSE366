import pygame

class Environment:
    BACKGROUND_COLOR = (255, 255, 255)
    AGENT_COLOR = (0, 128, 255) 
    TEXT_COLOR = (0, 0, 0)
    
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 36)
        pygame.display.set_caption("Pygame AI Simulation Assignment")

    def limit_position(self, x, y):
        if x < 0:
            x = 0
        elif x > self.width:
            x = self.width

        if y < 0:
            y = 0
        elif y > self.height:
            y = self.height

        return x, y



