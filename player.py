import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, play_area_rect):
        super().__init__()

        self.play_area_rect = play_area_rect

        # [수정] 플레이어 이미지 로드
        try:
            # .png 파일이므로 .convert_alpha() 사용 (투명도 지원)
            original_image = pygame.image.load("img/character.png").convert_alpha()

            # 이미지 비율 유지하면서 너비 40픽셀로 조정
            self.image_width = 70
            self.image_height = int(original_image.get_height() * (self.image_width / original_image.get_width()))
            self.image = pygame.transform.scale(original_image, (self.image_width, self.image_height))
        except FileNotFoundError:
            print("경고: 'img/character.png' 파일을 찾을 수 없습니다. 기본 파스텔 블루 사각형으로 실행됩니다.")
            self.image = pygame.Surface([40, 10])  # 기본 사각형 크기
            self.image.fill(PASTEL_BLUE)

        self.rect = self.image.get_rect()
        self.reset(play_area_rect)  # 초기 위치 설정 (아래 reset 함수 호출)

        self.speed = 5  # 플레이어 이동 속도

    def reset(self, play_area_rect):
        self.play_area_rect = play_area_rect
        # 플레이어를 게임 영역의 중앙 하단에 위치
        self.rect.centerx = self.play_area_rect.centerx

        #
        # [수정] Y 위치: 5픽셀 틈 제거, 맨 밑으로
        #
        self.rect.bottom = self.play_area_rect.bottom + 15
        # (기존 코드: self.play_area_rect.bottom - 5)

    def update(self):
        # 키 입력 처리
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # 화면 밖으로 나가지 않도록 제한 (PLAY_AREA_RECT 기준)
        if self.rect.left < self.play_area_rect.left:
            self.rect.left = self.play_area_rect.left
        if self.rect.right > self.play_area_rect.right:
            self.rect.right = self.play_area_rect.right

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def get_pos(self):
        # 총알 발사 위치 (이미지의 중앙 상단)ㄴ
        return self.rect.centerx, self.rect.top