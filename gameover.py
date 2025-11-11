# game_over.py
import pygame
import sys

def game_over_screen(screen, clock, nextBtn, game_over_img, background, WIDTH, HEIGHT):
    # 'restartText' 텍스트의 사각형 위치를 계산
    nextBtn_rect = nextBtn.get_rect(center=(WIDTH *0.85, HEIGHT * 0.9))
    gameoverimg_rect = game_over_img.get_rect(center=(WIDTH / 2, HEIGHT * 0.43))

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'QUIT'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # 'restartText_rect'의 클릭 감지
                    if nextBtn_rect.collidepoint(event.pos):
                        return 'GO_START'

        screen.blit(background, (0, 0))
        screen.blit(game_over_img, gameoverimg_rect)
        screen.blit(nextBtn, nextBtn_rect)

        pygame.display.update()
        clock.tick(60)