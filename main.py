import pygame
import sys
import start
import gameover

screen = None
clock = None
owlMain = None
owlStart = None
acorn = None
background = None
startBtn = None
wordshot = None
restartText = None
gameoverImg = None
quitText = None
WIDTH, HEIGHT = 800, 600


def drawObject(obj, x, y):
    global screen
    screen.blit(obj, (x, y))


def initGame():
    # --- (2. 수정) global 목록에 'restartText' 추가 ---
    global screen, clock, background, owlMain, owlStart, acorn, startBtn, wordshot, quitText, gameoverImg, restartText

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("WordShot")
    background = pygame.image.load('./img/background.jpg')
    acorn = pygame.image.load('./img/acorn.png')
    startBtn = pygame.image.load("./img/start.png")
    owlStart = pygame.image.load('./img/owl.png')

    owlMain = pygame.image.load('./img/owl.png')
    owlMain = pygame.transform.scale(owlStart, (100, 100))

    wordshot = pygame.image.load('img/wordshot.png')
    wordshot = pygame.transform.scale(wordshot, (420, 130))

    gameoverImg = pygame.image.load('./img/gameover.png')

    # --- (3. 수정) 'restart.png' 로드 대신 "Restart" 텍스트 생성 ---
    restartFont = pygame.font.Font(None, 50)  # 폰트 크기 50
    restartText = restartFont.render('Restart', True, (255, 255, 255))  # 흰색

    quitFont = pygame.font.Font(None, 40)
    quitText = quitFont.render('End Game', True, (255, 0, 0))

    clock = pygame.time.Clock()


def runGame():
    # ... (runGame 함수는 수정할 필요 없음) ...
    # ... (이전과 동일한 runGame 코드) ...
    global screen, clock, background, owlMain, acorn, quitText
    owlSize = owlMain.get_rect().size
    owlWidth = owlSize[0]
    owlHeight = owlSize[1]
    x = WIDTH * 0.45
    y = HEIGHT * 0.83
    owlX = 0
    acornXY = []  # 무기 좌표 리스트
    quitText_rect = quitText.get_rect(bottomright=(WIDTH - 10, HEIGHT - 10))
    onGame = True
    while onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                onGame = False
                return 'QUIT'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if quitText_rect.collidepoint(event.pos):
                        onGame = False
                        return 'GAME_OVER'
            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:
                    owlX = -3
                elif event.key == pygame.K_RIGHT:
                    owlX = 3
                elif event.key == pygame.K_SPACE:
                    acornX = x + owlWidth / 2
                    acornY = y
                    acornXY.append([acornX, acornY])
                elif event.key == pygame.K_g:
                    onGame = False
                    return 'GAME_OVER'
            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    owlX = 0
        x += owlX
        if x < 0:
            x = 0
        elif x > WIDTH - owlWidth:
            x = WIDTH - owlWidth
        drawObject(background, 0, 0)
        drawObject(owlMain, x, y)
        if len(acornXY) != 0:
            new_acornXY = []
            for bxy in acornXY:
                bxy[1] -= 10
                if bxy[1] > 0:
                    new_acornXY.append(bxy)
            acornXY = new_acornXY
        if len(acornXY) != 0:
            for bx, by in acornXY:
                drawObject(acorn, bx, by)
        screen.blit(quitText, quitText_rect)
        pygame.display.update()
        clock.tick(60)
    return 'QUIT'


if __name__ == "__main__":
    initGame()
    gameStart = start.startScreen(screen, clock, background, startBtn, owlStart, wordshot, WIDTH, HEIGHT)

    if not gameStart:
        pygame.quit()
        sys.exit()

    while True:
        game_status = runGame()

        if game_status == 'GAME_OVER':
            next_action = gameover.game_over_screen(screen, clock, restartText, gameoverImg, WIDTH, HEIGHT)

            if next_action == 'RESTART':
                continue
            else:
                break

        elif game_status == 'QUIT':
            break

    pygame.quit()
    sys.exit()