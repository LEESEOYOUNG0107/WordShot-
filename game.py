import pygame
import random
import time
from settings import *
from player import Player
from enemy import Enemy
from bullet import Bullet


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect()

        try:
            # 'background.png' 로드
            self.game_background_image = pygame.image.load("img/background.png").convert_alpha()
            self.game_background_image = pygame.transform.scale(self.game_background_image,
                                                                (SCREEN_WIDTH, SCREEN_HEIGHT))
        except FileNotFoundError:
            print("경고: 'img/background.png' 파일을 찾을 수 없습니다.")
            self.game_background_image = None

        pygame.key.set_repeat(500, 30)
        pygame.display.set_caption("WordShot")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "START"

        self.saja_list = [
            {"word": "고진감래", "meaning": "고생 끝에 낙이 온다"},
            {"word": "동고동락", "meaning": "고통과 즐거움을 함께 한다"},
            {"word": "유비무환", "meaning": "미리 준비하면 근심이 없다"},
            {"word": "과유불급", "meaning": "지나친 것은 미치지 못한 것과 같다"},
            {"word": "다다익선", "meaning": "많으면 많을수록 좋다"},
            {"word": "일석이조", "meaning": "한 가지 일로 두 가지 이익을 얻음"},
            {"word": "자화자찬", "meaning": "자기가 한 일을 스스로 칭찬함"},
        ]

        self.player = Player(PLAY_AREA_RECT)
        self.reset_game_variables()

    def reset_game_variables(self):
        self.player.reset(PLAY_AREA_RECT)
        self.bullets = []
        self.enemies = []
        self.bullet_count = 0
        self.user_input = ""
        self.current_saja = random.choice(self.saja_list)
        self.score = 0
        self.correct_saja_list = []
        self.lives = 3
        self.last_enemy_spawn_time = time.time()
        self.enemy_spawn_interval = 4.0

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.game_state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    self.handle_playing_keydown(event)
                elif event.type == pygame.TEXTINPUT:
                    char = event.text
                    if '\uac00' <= char <= '\ud7a3':
                        self.user_input += char

            elif self.game_state == "START":
                if event.type == pygame.MOUSEBUTTONDOWN and self.start_button_rect.collidepoint(event.pos):
                    self.reset_game_variables()
                    self.game_state = "PLAYING"
                    pygame.key.start_text_input()
            elif self.game_state == "GAME_OVER":
                if event.type == pygame.MOUSEBUTTONDOWN and self.restart_button_rect.collidepoint(event.pos):
                    self.game_state = "START"
                    pygame.key.stop_text_input()

    def handle_playing_keydown(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.user_input = self.user_input[:-1]
        elif event.key == pygame.K_RETURN:
            if self.user_input == self.current_saja["word"]:
                player_pos = self.player.get_pos()
                self.bullets.append(Bullet(player_pos[0], player_pos[1]))

                if self.current_saja["word"] not in self.correct_saja_list:
                    self.correct_saja_list.append(self.current_saja["word"])

                new_saja = random.choice(self.saja_list)
                while new_saja == self.current_saja:
                    new_saja = random.choice(self.saja_list)
                self.current_saja = new_saja
            self.user_input = ""

    def update(self):
        if self.game_state != "PLAYING":
            return

        self.player.update()

        for bullet in self.bullets:
            bullet.update()
            if bullet.rect.bottom < PLAY_AREA_RECT.top:
                self.bullets.remove(bullet)

        current_time = time.time()
        if current_time - self.last_enemy_spawn_time > self.enemy_spawn_interval:
            self.enemies.append(Enemy(PLAY_AREA_RECT))
            self.last_enemy_spawn_time = current_time

            if self.score > 50 and self.enemy_spawn_interval > 2.0:
                self.enemy_spawn_interval -= 0.1
            elif self.score > 100 and self.enemy_spawn_interval > 1.5:
                self.enemy_spawn_interval -= 0.1
            self.enemy_spawn_interval = max(self.enemy_spawn_interval, 1.0)  # 0.7 -> 1.0 (영역이 좁아져서)

        for enemy in self.enemies:
            enemy.update()
            if enemy.rect.top > PLAY_AREA_RECT.bottom:
                self.enemies.remove(enemy)
                self.lives -= 1

        if self.lives <= 0:
            self.game_state = "GAME_OVER"
            pygame.key.stop_text_input()

        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect.inflate(10, 10)):  # 30->10
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    break

    def draw(self):
        # 1. 검은색 배경
        self.screen.fill(BLACK)
        # 2. 전체 배경 그리기 (background.png)
        if self.game_background_image:
            self.screen.blit(self.game_background_image, (0, 0))
        else:
            # 배경 없으면, 게임 영역만 검게
            pygame.draw.rect(self.screen, BLACK, PLAY_AREA_RECT)

        # 3. 게임 상태에 맞게 그리기
        if self.game_state == "START":
            self.draw_start_screen()
        elif self.game_state == "PLAYING":
            self.draw_playing_screen()
        elif self.game_state == "GAME_OVER":
            self.draw_game_over_screen()

        pygame.display.flip()

    def draw_start_screen(self):
        # [수정] 시작 화면 요소들을 '게임 영역(PLAY_AREA_RECT)' 중앙에 배치
        title_text = FONT_LARGE.render("WordShot", True, WHITE)
        title_rect = title_text.get_rect(center=(PLAY_AREA_RECT.centerx, PLAY_AREA_RECT.centery - 40))
        self.screen.blit(title_text, title_rect)

        # [수정] 버튼 크기 및 위치 조절
        self.start_button_rect = pygame.Rect(0, 0, 150, 40)  # 200x50 -> 150x40
        self.start_button_rect.center = (PLAY_AREA_RECT.centerx, PLAY_AREA_RECT.centery + 30)

        pygame.draw.rect(self.screen, MINT, self.start_button_rect)
        start_text = FONT_MEDIUM.render("게임 시작", True, WHITE)
        start_text_rect = start_text.get_rect(center=self.start_button_rect.center)
        self.screen.blit(start_text, start_text_rect)

    def draw_playing_screen(self):
        # --- 게임 요소 그리기 (PLAY_AREA_RECT 안에서) ---
        self.player.draw(self.screen)

        # [수정] 총알/적이 PLAY_AREA_RECT와 겹칠 때만 그리기
        for bullet in self.bullets:
            if bullet.rect.colliderect(PLAY_AREA_RECT):
                bullet.draw(self.screen)
        for enemy in self.enemies:
            if enemy.rect.colliderect(PLAY_AREA_RECT):
                enemy.draw(self.screen)

        # --- [수정] UI 그리기 (settings.py에서 정의한 PLAY_AREA_RECT 기준) ---

        # 사자성어와 뜻 (settings.py의 SAJA_WORD_POS, SAJA_MEANING_POS 사용)
        saja_text = FONT_MEDIUM.render(self.current_saja['word'], True, WHITE)
        saja_rect = saja_text.get_rect(center=SAJA_WORD_POS)
        self.screen.blit(saja_text, saja_rect)

        meaning_text = FONT_SMALL.render(self.current_saja['meaning'], True, WHITE)
        meaning_rect = meaning_text.get_rect(center=SAJA_MEANING_POS)
        self.screen.blit(meaning_text, meaning_rect)

        # [수정] 입력창 (PLAY_AREA_RECT 중앙 하단 기준)
        input_text = FONT_MEDIUM.render(self.user_input, True, PASTEL_YELLOW)
        underline_width = max(100, input_text.get_width() + 10)  # 20->10

        # X 위치: settings.py의 UI_CENTER_X (PLAY_AREA_RECT.centerx) 사용
        underline_pos_start = (UI_CENTER_X - underline_width // 2, INPUT_BOX_Y + 5)
        underline_pos_end = (UI_CENTER_X + underline_width // 2, INPUT_BOX_Y + 5)
        pygame.draw.line(self.screen, PASTEL_YELLOW, underline_pos_start, underline_pos_end, 2)

        # Y 위치: settings.py의 INPUT_BOX_Y 사용
        input_rect = input_text.get_rect(midbottom=(UI_CENTER_X, INPUT_BOX_Y))
        self.screen.blit(input_text, input_rect)

        # 점수 (settings.py의 SCORE_POS 사용)
        score_text = FONT_GUI.render(f"{self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=SCORE_POS)
        self.screen.blit(score_text, score_rect)

        # 목숨 (settings.py의 LIVES_POS 사용)
        lives_text = FONT_GUI.render(f"LIVES: {self.lives}", True, WHITE)
        lives_rect = lives_text.get_rect(center=LIVES_POS)
        self.screen.blit(lives_text, lives_rect)

    def draw_game_over_screen(self):
        # [수정] 게임 오버 화면 요소들을 '게임 영역(PLAY_AREA_RECT)' 중앙에 배치
        game_over_text = FONT_LARGE.render("게임 오버", True, PASTEL_PINK)
        game_over_rect = game_over_text.get_rect(center=(PLAY_AREA_RECT.centerx, PLAY_AREA_RECT.top + 40))
        self.screen.blit(game_over_text, game_over_rect)

        final_score_text = FONT_MEDIUM.render(f"최종 점수: {self.score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(PLAY_AREA_RECT.centerx, game_over_rect.bottom + 30))
        self.screen.blit(final_score_text, final_score_rect)

        correct_list_text = FONT_SMALL.render("맞춘 사자성어:", True, PASTEL_YELLOW)
        correct_list_rect = correct_list_text.get_rect(center=(PLAY_AREA_RECT.centerx, final_score_rect.bottom + 30))
        self.screen.blit(correct_list_text, correct_list_rect)

        # [수정] 맞춘 사자성어 목록 나열 (PLAY_AREA_RECT 기준)
        start_x = PLAY_AREA_RECT.left + 10  # 게임 영역 왼쪽 여백
        current_x = start_x
        current_y = correct_list_rect.bottom + 10
        for i, word in enumerate(self.correct_saja_list):
            word_text = FONT_SMALL.render(word, True, WHITE)
            word_rect = word_text.get_rect(topleft=(current_x, current_y))

            # [수정] 줄바꿈 기준을 PLAY_AREA_RECT.right로
            if word_rect.right > PLAY_AREA_RECT.right - 10:  # 게임 영역 오른쪽 여백
                current_y += word_rect.height + 3  # 줄 간격
                current_x = start_x
                word_rect.topleft = (current_x, current_y)

            # [수정] Y좌표가 버튼을 침범하지 않게
            if word_rect.bottom > PLAY_AREA_RECT.bottom - 50:
                break  # 너무 길면 그만 그림

            self.screen.blit(word_text, word_rect)
            current_x = word_rect.right + 10  # 단어 사이 간격

        # [수정] '처음으로' 버튼 (PLAY_AREA_RECT 하단)
        self.restart_button_rect = pygame.Rect(0, 0, 150, 40)  # 200x50 -> 150x40
        self.restart_button_rect.center = (PLAY_AREA_RECT.centerx, PLAY_AREA_RECT.bottom - 25)

        pygame.draw.rect(self.screen, MINT, self.restart_button_rect)
        restart_text = FONT_MEDIUM.render("처음으로", True, WHITE)
        restart_text_rect = restart_text.get_rect(center=self.restart_button_rect.center)
        self.screen.blit(restart_text, restart_text_rect)