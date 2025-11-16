import pygame
import random
from settings import *


class Enemy(pygame.sprite.Sprite):
    # 'current_score'를 인수로 받습니다.
    def __init__(self, play_area_rect, current_score):
        super().__init__()

        self.play_area_rect = play_area_rect

        # (이미지 로드 코드는 수정 없음)
        try:
            original_image = pygame.image.load("img/enemy.png").convert_alpha()
            self.image_width = 30
            self.image_height = int(original_image.get_height() * (self.image_width / original_image.get_width()))
            self.image = pygame.transform.scale(original_image, (self.image_width, self.image_height))
        except FileNotFoundError:
            print("경고: 'img/enemy.png' 파일을 찾을 수 없습니다. 기본 파스텔 핑크 사각형으로 실행됩니다.")
            self.image = pygame.Surface([30, 30])
            self.image.fill(PASTEL_PINK)

        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(self.play_area_rect.left, self.play_area_rect.right - self.rect.width)
        self.rect.bottom = self.play_area_rect.top

        # --- [수정] 50점 단위로 속도(speed)를 다르게 설정 ---
        if current_score >= 200:
            self.speed = 5  # Level 5 (매우 빠름)
        elif current_score >= 150:
            self.speed = 4  # Level 4
        elif current_score >= 100:
            self.speed = 3  # Level 3
        elif current_score >= 50:
            self.speed = 2  # Level 2
        else:
            self.speed = 1  # Level 1 (느림)
        # --- [수정 완료] ---

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)