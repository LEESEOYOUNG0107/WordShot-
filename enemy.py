import pygame
import random
from settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, play_area_rect):
        super().__init__()

        self.play_area_rect = play_area_rect

        # [수정] 적 이미지 로드
        try:
            # [수정] .png 파일이므로 .convert_alpha() 사용 (투명도 지원)
            original_image = pygame.image.load("img/enemy.png").convert_alpha()

            # 이미지 비율 유지하면서 너비 30픽셀로 조정
            self.image_width = 30
            self.image_height = int(original_image.get_height() * (self.image_width / original_image.get_width()))
            self.image = pygame.transform.scale(original_image, (self.image_width, self.image_height))
        except FileNotFoundError:
            # [수정] 오류 메시지도 .png로 변경
            print("경고: 'img/enemy.png' 파일을 찾을 수 없습니다. 기본 파스텔 핑크 사각형으로 실행됩니다.")
            self.image = pygame.Surface([30, 30])  # 기본 사각형 크기
            self.image.fill(PASTEL_PINK)

        self.rect = self.image.get_rect()

        # 적은 게임 영역 상단에서 랜덤하게 등장
        self.rect.x = random.randrange(self.play_area_rect.left, self.play_area_rect.right - self.rect.width)
        self.rect.y = self.play_area_rect.top - self.rect.height  # 게임 영역 바로 위에서 시작

        self.speed = random.randrange(1, 3)  # 적 이동 속도 (1~2)

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)