import pygame
from settings import *

class Player:
    def __init__(self):
        self.width = 50
        self.height = 20
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 70
        self.speed = 7
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)

    def reset(self):
        self.rect.x = SCREEN_WIDTH // 2 - self.width // 2
        self.rect.y = SCREEN_HEIGHT - 70

    def get_pos(self):
        return self.rect.midtop