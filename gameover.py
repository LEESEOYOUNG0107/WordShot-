# game_over.py
import pygame
import sys

def game_over_screen(screen, clock, restartText, game_over_img, WIDTH, HEIGHT):
    # 'restartText' 텍스트의 사각형 위치를 계산
    restartText_rect = restartText.get_rect(center=(WIDTH / 2, HEIGHT * 0.75))
    gameoverimg = game_over_img.get_rect(center = (WIDTH / 2, HEIGHT * 0.43))

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'QUIT'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # 'restartText_rect'의 클릭 감지
                    if restartText_rect.collidepoint(event.pos):
                        return 'RESTART'

        screen.blit(game_over_img, gameoverimg)
        screen.blit(restartText, restartText_rect)

        pygame.display.update()
        clock.tick(60)