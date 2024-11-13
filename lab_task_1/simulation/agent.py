import pygame
from environment import Environment

class Agent(pygame.sprite.Sprite):
    width = 30
    height = 30
    def __init__(self, x_position, y_position, speed, env):
        super().__init__()
        self.speed = speed
        self.env = env
        self.image = pygame.Surface((Agent.width, Agent.height))
        self.image.fill(self.env.AGENT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x_position
        self.rect.y = y_position

    def move(self, dir):
        self.speed += 1 

        if dir == "left":
            self.rect.x = (self.rect.x - self.speed + self.env.width) % self.env.width
        elif dir == "right":
            self.rect.x = (self.rect.x + self.speed) % self.env.width
        elif dir == "up":
            self.rect.y = (self.rect.y - self.speed + self.env.height) % self.env.height
        else:
            self.rect.y = (self.rect.y + self.speed) % self.env.height

        self.rect.x, self.rect.y = self.env.limit_position(self.rect.x, self.rect.y)
