import pygame
import sys
import start
import gameover
import random

screen = None
clock = None
owlMain = None
owlStart = None
acorn = None
background = None
startBtn = None
wordshot = None
nextBtn = None
gameoverImg = None
quitText = None
explosion = None
heartImg = None
WIDTH, HEIGHT = 800, 600
robotImg = ['./img/robot (1).png', './img/robot (2).png', './img/robot (3).png', ]


def drawObject(obj, x, y):
    global screen
    screen.blit(obj, (x, y))


def initGame():
    global screen, clock, background, owlMain, owlStart, acorn, startBtn, wordshot, \
        quitText, gameoverImg, nextBtn, explosion, heartImg

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("WordShot")
    background = pygame.image.load('./img/background.jpg')
    acorn = pygame.image.load('./img/acorn.png')
    startBtn = pygame.image.load("./img/start.png")
    startBtn = pygame.transform.scale(startBtn, (300, 100))

    owlStart = pygame.image.load('./img/owl.png')

    owlMain = pygame.image.load('./img/owl.png')
    owlMain = pygame.transform.scale(owlStart, (100, 100))

    wordshot = pygame.image.load('img/wordshot.png')
    wordshot = pygame.transform.scale(wordshot, (420, 130))

    gameoverImg = pygame.image.load('./img/gameover.png')

    nextBtn = pygame.image.load('./img/next.png')

    quitFont = pygame.font.Font(None, 40)
    quitText = quitFont.render('End Game', True, (255, 0, 0))

    explosion = pygame.image.load('./img/explosion.png')
    heartImg = pygame.image.load('./img/heart.png')

    clock = pygame.time.Clock()


def runGame():
    global screen, clock, background, owlMain, acorn, quitText, explosion, heartImg

    owlSize = owlMain.get_rect().size
    owlWidth = owlSize[0]
    owlHeight = owlSize[1]

    # 도토리 크기를 미리 가져옵니다 (충돌 감지에 사용)
    acornSize = acorn.get_rect().size
    acornWidth = acornSize[0]
    acornHeight = acornSize[1]

    heartSize = heartImg.get_rect().size
    heartWidth = heartSize[0]
    lives = 3

    x = WIDTH * 0.45
    y = HEIGHT * 0.83
    owlX = 0
    acornXY = []  # 무기 좌표 리스트

    robot = pygame.image.load(random.choice(robotImg))
    robotSize = robot.get_rect().size
    robotWith = robotSize[0]
    robotHeight = robotSize[1]
    robotX = random.randrange(0, WIDTH - robotWith)
    robotY = 0
    robotSpeed = 2

    isShot = False
    shotCount = 0

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
                    owlX = -5
                elif event.key == pygame.K_RIGHT:
                    owlX = 5
                elif event.key == pygame.K_SPACE:
                    acornX = x + owlWidth / 2
                    acornY = y
                    acornXY.append([acornX, acornY])
                # elif event.key == pygame.K_g:
                #     onGame = False
                #     return 'GAME_OVER'
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

        # 도토리 이동 및 충돌 감지 로직
        if len(acornXY) != 0:
            new_acornXY = []
            for bxy in acornXY:
                bxy[1] -= 10  # 1. 도토리 이동
                is_hit = False  # 이 도토리가 맞았는지 확인용

                # 로봇이 살아있을 때(isShot=False)만 충돌 검사
                if not isShot:
                    acorn_rect = pygame.Rect(bxy[0], bxy[1], acornWidth, acornHeight)
                    robot_rect = pygame.Rect(robotX, robotY, robotWith, robotHeight)

                    # 두 사각형이 충돌했는지 검사
                    if acorn_rect.colliderect(robot_rect):
                        is_hit = True  # 이 도토리는 사라짐
                        isShot = True  # 로봇이 맞은 상태로 변경
                        shotCount = 0  # 폭발 타이머 시작
                        #폭발 이미지를 얼마나 오랫동안 화면에 보여줄지 시간을 잼

                # 화면 안에 그리고 맞지 않았을 때만
                if bxy[1] > 0 and not is_hit:
                    new_acornXY.append(bxy)  # 새 리스트에 추가
            acornXY = new_acornXY  # 리스트를 새것으로 교체

        if len(acornXY) != 0:
            for bx, by in acornXY:
                drawObject(acorn, bx, by)

        #부엉이 로봇 충돌 감지
        owlMain_rect = pygame.Rect(x, y, owlWidth, owlHeight)
        robot_rect = pygame.Rect(robotX, robotY, robotWith, robotHeight)

        # 로봇이 살아있고(not isShot), 부엉이와 충돌했다면
        if not isShot and owlMain_rect.colliderect(robot_rect):
            lives -= 1
            isShot = True #로봇 폭발
            shotCount = 0

        # 로봇/폭발 그리기
        if not isShot:
            # 로봇이 살아있을 때
            robotY += robotSpeed  # 로봇 아래로 움직임
            if robotY > HEIGHT:
                lives -= 1
                # 새로운 로봇(랜덤)
                robot = pygame.image.load(random.choice(robotImg))
                robotSize = robot.get_rect().size
                robotWith = robotSize[0]
                robotHeight = robotSize[1]
                robotX = random.randrange(0, WIDTH - robotWith)
                robotY = 0

                #로봇 맞추면 속도 증가
                robotSpeed += 0.2
                if robotSpeed >= 10 :
                    robotSpeed = 10

            drawObject(robot, robotX, robotY)  # 로봇 그리기
        else:
            # (로봇이 맞았을 때)
            drawObject(explosion, robotX, robotY)  # 폭발 그리기
            shotCount += 1  # 2. 폭발 타이머 증가

            if shotCount > 30:  # 30프레임(0.5초)이 지나면
                isShot = False  # 로봇을 다시 '살아있는' 상태로
                # 새 로봇 생성
                robot = pygame.image.load(random.choice(robotImg))
                robotSize = robot.get_rect().size
                robotWith = robotSize[0]
                robotHeight = robotSize[1]
                robotX = random.randrange(0, WIDTH - robotWith)
                robotY = 0

        for i in range (lives):
            drawObject(heartImg, 10+i*(heartWidth+5), 10)

        if lives <= 0:
            onGame = False
            return 'GAME_OVER'

        screen.blit(quitText, quitText_rect)
        pygame.display.update()
        clock.tick(60)
    return 'QUIT'


if __name__ == "__main__":
    initGame()
    while True:
        gameStart = start.startScreen(screen, clock, background, startBtn, owlStart, wordshot, WIDTH, HEIGHT)
        if not gameStart: # 시작 화면에서 X를 누르면
            break;

        game_running = True
        while game_running:
            game_status = runGame()

            if game_status == 'GAME_OVER':
                next_action = gameover.game_over_screen(screen, clock, nextBtn, gameoverImg, background, WIDTH, HEIGHT)

                if next_action == 'GO_START': #GO_START를 받으면
                    game_running = False # '게임 플레이 루프'만 탈출
                else:
                    game_running = False # 게임 플레이 루프 탈출
                    gameStart = False # 메인 앱 루프도 탈출

            elif game_status == 'QUIT':
                game_running = False # 게임 플레이 루프 탈출
                gameStart = False # 메인 앱 루프도 탈출하도록

        if not gameStart:
            break
pygame.quit()
sys.exit()

# 다음에 할 거
# 놓친 횟수를 하트 3개로 목숨을 표시하도록 main.py 파일을 수정하기