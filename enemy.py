import pygame
import random
from settings import *

class Enemy:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = 0
        self.speed = 4
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)