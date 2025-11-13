import pygame, sys, start, gameover, random, math

screen = clock = owlMain = owlStart = acorn = background = startBtn = wordshot = nextBtn = gameoverImg = quitText = explosion = \
    heartImg = acornSound = gameoverSound = typingFont = None
WIDTH, HEIGHT = 800, 600
robotImg = ['./img/robot (1).png', './img/robot (2).png', './img/robot (3).png', ]


def drawObject(obj, x, y):
    global screen
    screen.blit(obj, (x, y))


def initGame():
    global screen, clock, background, owlMain, owlStart, acorn, startBtn, wordshot, quitText, gameoverImg, nextBtn, explosion, heartImg, acornSound, gameoverSound, typingFont, robotFont

    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
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

    pygame.mixer.music.load('./sound/music2.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

    acornSound = pygame.mixer.Sound('./sound/acorn.mp3')
    acornSound.set_volume(0.05)
    gameoverSound = pygame.mixer.Sound('./sound/gameover.mp3')

    fontPath = './font/NanumGothicBold.otf'
    typingFont = pygame.font.Font(fontPath, 30)

    robotFont = pygame.font.Font(fontPath, 15)

    clock = pygame.time.Clock()

def runGame():
    global screen, clock, background, owlMain, acorn, quitText, explosion, heartImg, acornSound, gameoverSound, typingFont, robotFont

    pygame.key.start_text_input()

    owlSize = owlMain.get_rect().size
    owlWidth = owlSize[0]
    owlHeight = owlSize[1]

    acornSize = acorn.get_rect().size
    acornWidth = acornSize[0]
    acornHeight = acornSize[1]

    heartSize = heartImg.get_rect().size
    heartWidth = heartSize[0]
    lives = 3

    x = WIDTH * 0.45
    y = HEIGHT * 0.83

    # (1. 퀴즈 데이터)
    sajaData_list = [
        {"meaning": "겉과 속이 다름", "answer": "표리부동"},
        {"meaning": "돌 하나로\n두 마리 새를 잡음", "answer": "일석이조"},
        {"meaning": "바람 앞의 등불\n(매우 위태로움)", "answer": "풍전등화"},
        {"meaning": "지나친 것은\n모자란 것과 같음", "answer": "과유불급"},
        {"meaning": "죽어서도 은혜를\n잊지 않고 갚음", "answer": "결초보은"},
        {"meaning": "인생의 길흉화복은\n예측하기 어려움", "answer": "새옹지마"},
        {"meaning": "둘이 다투는 사이\n제삼자가 이익을 봄", "answer": "어부지리"},
        {"meaning": "아무 관계없는\n딴소리를 함", "answer": "동문서답"}
    ]
    robot_list = []
    currentTyping = ""
    score = 0
    animBullets = []
    base_speed = 0.1  # (난이도)

    targetMeaning = ""
    targetWord = ""

    def spawn_new_wave():
        nonlocal robot_list, base_speed
        robot_list.clear()  # 기존 로봇 (죽은 로봇) 모두 삭제

        initial_words = random.sample([d["answer"] for d in sajaData_list], 4) # 4개의 "겹치지 않는" 단어 선택

        for i in range(4):
            robot_list.append({
                'img': pygame.image.load(random.choice(robotImg)),
                'word': initial_words[i],
                'x': 100 + (i * 170),  # X좌표 (100, 270, 440, 610)
                'y': random.randint(-150, -50),
                'speed': base_speed + (random.random() * 0.5),  # (난이도 적용)
                'isShot': False,
                'shotCount': 0
            })

    def set_new_target(): # 남아있는 로봇 중 새 타겟 정하기
        nonlocal targetMeaning, targetWord

        # 'isShot=False' 살아있는 로봇들만 후보
        remaining_robots = [r for r in robot_list if not r['isShot']]

        if remaining_robots:
            new_target_robot = random.choice(remaining_robots)
            targetWord = new_target_robot['word']

            # 퀴즈 DB에서 뜻 찾기
            for item in sajaData_list:
                if item["answer"] == targetWord:
                    targetMeaning = item["meaning"]
                    break
            return True
        else: # (살아있는 로봇이 없음)
            return False

    spawn_new_wave()
    set_new_target()

    quitText_rect = quitText.get_rect(bottomright=(WIDTH - 10, HEIGHT - 10))
    onGame = True

    while onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                onGame = False
                pygame.key.stop_text_input()
                return 'QUIT'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if quitText_rect.collidepoint(event.pos):
                        pygame.mixer.music.stop()
                        gameoverSound.play()
                        onGame = False
                        pygame.key.stop_text_input()
                        return 'GAME_OVER'

            # K_SPACE' 정답 확인
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    typed_word = currentTyping.strip()
                    print(f"입력: {currentTyping}, 타겟: {targetWord}, 같음? {currentTyping == targetWord}")

                    if typed_word == "":
                        currentTyping = ""

                    else:
                        found_robot = None
                        for robot in robot_list:
                            if (not robot['isShot']) and robot['word'].strip() == typed_word:
                                found_robot = robot
                                break

                        if found_robot:
                            print(f"로봇 찾음! 로봇 단어: {found_robot['word']}")
                            if found_robot['word'].strip() == (targetWord or "").strip():
                                found_robot['isShot'] = True  # (정답!) 폭발 시작
                                found_robot['shotCount'] = 0
                                score += 1
                                acornSound.play()
                                base_speed += 0.05  # (난이도 상승!)

                            # (총알 발사)
                            animBullet_x = x + owlWidth / 2
                            animBullet_y = y
                            target_x = found_robot['x'] + found_robot['img'].get_width() / 2
                            target_y = found_robot['y'] + found_robot['img'].get_height() / 2
                            dx = target_x - animBullet_x
                            dy = target_y - animBullet_y
                            dist = max(1, math.sqrt(dx ** 2 + dy ** 2))
                            bullet_speed = 20
                            move_x = (dx / dist) * bullet_speed
                            move_y = (dy / dist) * bullet_speed
                            animBullets.append({'x': animBullet_x, 'y': animBullet_y,
                                                'move_x': move_x, 'move_y': move_y,
                                                'target_x': target_x, 'target_y': target_y})

                            # 정답 맞힘 -> 다음 퀴즈 (남은 3개 중)
                            if not set_new_target():
                                # (False가 리턴됨 = 4마리 다 잡음)
                                targetMeaning = "WAVE CLEAR!"
                                targetWord = ""
                        else:
                            print("로봇 못 찾음!")
                    currentTyping = ""
                elif event.key == pygame.K_BACKSPACE:
                    currentTyping = currentTyping[:-1]

            elif event.type == pygame.TEXTINPUT:
                if len(currentTyping) < 10:
                    currentTyping += event.text

        drawObject(background, 0, 0)
        drawObject(owlMain, x, y)

        # 로봇 4개 그리기/이동/충돌
        all_robots_dead = True

        for robot in robot_list:
            owlMain_rect = pygame.Rect(x, y, owlWidth, owlHeight)
            robot_rect = pygame.Rect(robot['x'], robot['y'],
                                     robot['img'].get_width(), robot['img'].get_height())

            if not robot['isShot'] and owlMain_rect.colliderect(robot_rect):
                lives -= 1
                robot['isShot'] = True
                robot['shotCount'] = 0
                if robot['word'] == targetWord:
                    set_new_target()

            if not robot['isShot']:
                all_robots_dead = False  # (아직 살아있는 로봇 있음)

                robot['y'] += robot['speed']
                if robot['y'] > HEIGHT:
                    lives -= 1
                    robot['isShot'] = True  # (놓쳐도 죽은 처리)
                    robot['shotCount'] = 0  # (폭발 애니메이션 시작)
                    if robot['word'] == targetWord:
                        set_new_target()

                drawObject(robot['img'], robot['x'], robot['y'])

                word_text = robotFont.render(robot['word'], True, (255, 0, 0))
                word_rect = word_text.get_rect(center=(robot['x'] + robot['img'].get_width() / 2, robot['y'] + 31))
                screen.blit(word_text, word_rect)

            else:
                # (폭발 중)
                if robot['shotCount'] <= 30:
                    drawObject(explosion, robot['x'], robot['y'])
                    robot['shotCount'] += 1
                else:
                    pass

                    # 4마리 다 죽었으면 -> 새 웨이브!
        if all_robots_dead:
            base_speed += 0.1  # 난이도 상승폭
            animBullets.clear()
            currentTyping = ""
            spawn_new_wave()
            set_new_target()

        # (총알 그리기)
        new_animBullets = []
        for b in animBullets:
            b['x'] += b['move_x']
            b['y'] += b['move_y']

            dist_x_sq = (b['x'] - b['target_x']) ** 2
            dist_y_sq = (b['y'] - b['target_y']) ** 2
            current_dist = math.sqrt(dist_x_sq + dist_y_sq)

            if current_dist > 20:
                drawObject(acorn, b['x'], b['y'])
                new_animBullets.append(b)
        animBullets = new_animBullets

        # (타이핑 UI 그리기)
        meaningLines = targetMeaning.split('\n')
        lineSpacing = 5
        lineHeight = typingFont.get_height()

        for i, line in enumerate(meaningLines):
            targetText = typingFont.render(line, True, (255, 255, 255))
            y_pos = 50 + (i * (lineHeight + lineSpacing))
            target_rect = targetText.get_rect(center=(WIDTH / 2, y_pos))
            screen.blit(targetText, target_rect)

        typingText = typingFont.render(currentTyping, True, (255, 255, 0))
        typing_rect = typingText.get_rect(center=(WIDTH / 2, HEIGHT - 50))
        screen.blit(typingText, typing_rect)

        writeScore(score)

        for i in range(lives):
            drawObject(heartImg, (WIDTH - 10 - heartWidth) - i * (heartWidth + 5), 10)

        if lives <= 0:
            pygame.mixer.music.stop()
            gameoverSound.play()
            onGame = False
            pygame.key.stop_text_input()
            return 'GAME_OVER'

        screen.blit(quitText, quitText_rect)
        pygame.display.update()
        clock.tick(60)

    pygame.key.stop_text_input()
    return 'QUIT'

# 로봇을 맟준 개수 계산
def writeScore(count):
    global screen
    font = pygame.font.Font(None, 30)
    text = font.render('Score: ' + str(count), True, (255, 255, 255))
    screen.blit(text, (10, 10))


if __name__ == "__main__":
    initGame()
    while True:
        gameStart = start.startScreen(screen, clock, background, startBtn, owlStart, wordshot, WIDTH, HEIGHT)
        if not gameStart:
            break;
        pygame.mixer.music.play(-1)
        game_running = True
        while game_running:
            game_status = runGame()

            if game_status == 'GAME_OVER':
                next_action = gameover.game_over_screen(screen, clock, nextBtn, gameoverImg, background, WIDTH, HEIGHT)
                if next_action == 'GO_START':
                    game_running = False
                else:
                    game_running = False
                    gameStart = False
            elif game_status == 'QUIT':
                game_running = False
                gameStart = False
        if not gameStart:
            break

pygame.quit()
sys.exit()