import pygame
import sys

from numpy.core.defchararray import center

def startScreen(screen, clock, background, startBtn, owl, wardshot, WIDTH, HEIGHT):
    #'START'가 클릭되면 True를 반환하고, '종료'하면 False를 반환
    wardshot_rect = wardshot.get_rect(center = (WIDTH / 2, HEIGHT * 0.2))
    owl_rect = owl.get_rect(center = (WIDTH / 2, HEIGHT * 0.53))
    startBtn_rect = startBtn.get_rect(center = (WIDTH / 2, HEIGHT * 0.81))

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if startBtn_rect.collidepoint(event.pos):
                        return True

        screen.blit(background, (0, 0))
        screen.blit(wardshot, wardshot_rect)
        screen.blit(owl, owl_rect)
        screen.blit(startBtn, startBtn_rect)
        pygame.display.update()
        clock.tick(60)