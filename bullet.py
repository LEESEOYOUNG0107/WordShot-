import pygame
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # 총알 이미지 로드
        try:
            # .png 파일은 .convert_alpha() 사용
            original_image = pygame.image.load("img/bullet.png").convert_alpha()

            # 이미지 비율 유지하면서 너비 10픽셀로 조정
            self.image_width = 30
            self.image_height = int(original_image.get_height() * (self.image_width / original_image.get_width()))
            self.image = pygame.transform.scale(original_image, (self.image_width, self.image_height))
        except FileNotFoundError:
            print("경고: 'img/bullet.png' 파일을 찾을 수 없습니다. 기본 파스텔 옐로우 사각형으로 실행됩니다.")
            self.image = pygame.Surface([5, 15])  # 기본 사각형 크기
            self.image.fill(PASTEL_YELLOW)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y  # 플레이어의 상단(get_pos)에서 발사

        self.speed = -10  # 총알 이동 속도 (위로 올라가므로 음수)

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)