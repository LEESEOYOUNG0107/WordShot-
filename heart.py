import pygame
import random
from settings import *


class Heart(pygame.sprite.Sprite):
    def __init__(self, play_area_rect):
        super().__init__()

        self.play_area_rect = play_area_rect

        # 1. 하트 이미지 로드
        try:
            # .png 파일이므로 .convert_alpha() 사용 (투명도 지원)
            original_image = pygame.image.load("img/heart.png").convert_alpha()

            # 이미지 비율 유지하면서 너비 25픽셀로 조정
            self.image_width = 25
            self.image_height = int(original_image.get_height() * (self.image_width / original_image.get_width()))
            self.image = pygame.transform.scale(original_image, (self.image_width, self.image_height))
        except FileNotFoundError:
            print("경고: 'img/heart.png' 파일을 찾을 수 없습니다. 빨간색 사각형으로 실행됩니다.")
            self.image = pygame.Surface([25, 25])  # 기본 사각형 크기
            self.image.fill((255, 0, 0))  # 빨간색

        self.rect = self.image.get_rect()

        # 2. 하트 스폰 위치 (적과 동일)
        self.rect.x = random.randrange(self.play_area_rect.left, self.play_area_rect.right - self.rect.width)
        self.rect.y = self.play_area_rect.top - self.rect.height  # 게임 영역 바로 위에서 시작

        #
        # [수정] 하트 이동 속도를 '1'로 고정 (느리게)
        #
        self.speed = 1
        # (기존 코드: self.speed = random.randrange(1, 3))

    def update(self):
        # 3. 아래로 이동
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)