import pygame
from settings import *

class Bullet:
    def __init__(self, x, y):
        self.width = 10
        self.height = 20
        self.speed = 10
        self.rect = pygame.Rect(x - self.width // 2, y, self.width, self.height)

    def update(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, self.rect)