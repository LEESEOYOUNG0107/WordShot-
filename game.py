# C:/Users/LG/Documents/Word-Shot/game.py

def update(self):
    # ... (생략) ...

    current_time = time.time()
    if current_time - self.last_enemy_spawn_time > self.enemy_spawn_interval:
        self.enemies.append(Enemy())
        self.last_enemy_spawn_time = current_time

        # 점수 구간별로 난이도 조정
        if self.score > 50 and self.enemy_spawn_interval > 2.0:
            self.enemy_spawn_interval -= 0.1
        elif self.score > 100 and self.enemy_spawn_interval > 1.5:
            self.enemy_spawn_interval -= 0.1
        elif self.score > 200 and self.enemy_spawn_interval > 1.0:
            self.enemy_spawn_interval -= 0.1

        # 최소 간격 제한 (너무 빨라지는 것 방지)
        self.enemy_spawn_interval = max(self.enemy_spawn_interval, 0.7)

    # ... (생략) ...import pygame
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

        # 키 반복 기능 활성화 (딜레이 500ms, 반복 간격 30ms)
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

        self.player = Player()
        self.reset_game_variables()

    def reset_game_variables(self):
        self.player.reset()
        self.bullets = []
        self.enemies = []
        self.bullet_count = 0
        self.user_input = ""
        self.current_saja = random.choice(self.saja_list)
        self.score = 0
        self.correct_saja_list = []
        self.lives = 3 # 목숨 3개로 초기화
        self.last_enemy_spawn_time = time.time()
        self.enemy_spawn_interval = 4.0  # 초기 적 생성 간격을 4초로 늘려 더 여유롭게 만듭니다.

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
                    # 한글만 입력받도록 처리
                    char = event.text
                    # '가' ~ '힣' 사이의 한글 유니코드 범위 확인
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
                    pygame.key.stop_text_input() # 다시 시작 화면으로 갈 때 텍스트 입력 비활성화

    def handle_playing_keydown(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.user_input = self.user_input[:-1]
        elif event.key == pygame.K_RETURN:
            if self.user_input == self.current_saja["word"]:
                # 정답을 맞히면 총알이 즉시 발사되도록 변경!
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
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

        current_time = time.time()
        if current_time - self.last_enemy_spawn_time > self.enemy_spawn_interval:
            self.enemies.append(Enemy())
            self.last_enemy_spawn_time = current_time

            # 점수 구간별로 난이도 조정
            if self.score > 50 and self.enemy_spawn_interval > 2.0:
                self.enemy_spawn_interval -= 0.1
            elif self.score > 100 and self.enemy_spawn_interval > 1.5:
                self.enemy_spawn_interval -= 0.1
            elif self.score > 200 and self.enemy_spawn_interval > 1.0:
                self.enemy_spawn_interval -= 0.1

            # 최소 간격 제한 (너무 빨라지는 것 방지)
            self.enemy_spawn_interval = max(self.enemy_spawn_interval, 0.7)

        for enemy in self.enemies:
            enemy.update()

            if enemy.rect.top > SCREEN_HEIGHT:
                # 적이 바닥에 닿으면 목숨 감소
                self.enemies.remove(enemy)
                self.lives -= 1
            
        # 목숨이 0이 되면 게임 오버
        if self.lives <= 0:
            self.game_state = "GAME_OVER"
            if pygame.key.get_text_input_active(): # 텍스트 입력이 활성화 상태일 때만 비활성화
                pygame.key.stop_text_input()

        for bullet in self.bullets:
            for enemy in self.enemies:
                # 충돌 판정을 너그럽게 만듭니다. 적의 히트박스를 상하좌우 15픽셀씩 늘려서 판정합니다.
                # 이제 총알이 적을 스치기만 해도 맞출 수 있습니다.
                if bullet.rect.colliderect(enemy.rect.inflate(30, 30)):
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    break

    def draw(self):
        self.screen.fill(BG_COLOR)
        if self.game_state == "START":
            self.draw_start_screen()
        elif self.game_state == "PLAYING":
            self.draw_playing_screen()
        elif self.game_state == "GAME_OVER":
            self.draw_game_over_screen()
        pygame.display.flip()

    def draw_start_screen(self):
        title_text = FONT_LARGE.render("WordShot", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title_text, title_rect)

        self.start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
        pygame.draw.rect(self.screen, MINT, self.start_button_rect)
        start_text = FONT_MEDIUM.render("게임 시작", True, WHITE)
        start_text_rect = start_text.get_rect(center=self.start_button_rect.center)
        self.screen.blit(start_text, start_text_rect)

    def draw_playing_screen(self):
        self.player.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # UI
        pygame.draw.rect(self.screen, BLACK, [0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50])
        
        # 사자성어와 뜻을 분리해서 표시
        saja_text = FONT_MEDIUM.render(self.current_saja['word'], True, WHITE)
        saja_rect = saja_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 75))
        self.screen.blit(saja_text, saja_rect)

        meaning_text = FONT_SMALL.render(self.current_saja['meaning'], True, WHITE)
        meaning_rect = meaning_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 45))
        self.screen.blit(meaning_text, meaning_rect)

        # 입력창을 화면 하단, 사자성어 문제 바로 위에 배치
        input_text = FONT_MEDIUM.render(self.user_input, True, PASTEL_YELLOW) 
        # 밑줄(커서) 효과 추가
        underline_width = max(40, input_text.get_width() + 10) # 최소 40픽셀 보장
        underline_pos = (SCREEN_WIDTH // 2 - underline_width // 2, SCREEN_HEIGHT - 10)
        pygame.draw.line(self.screen, PASTEL_YELLOW, (underline_pos), (underline_pos[0] + underline_width, underline_pos[1]), 2)
        input_rect = input_text.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10))
        self.screen.blit(input_text, input_rect)

        score_text = FONT_SMALL.render(f"점수: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # 목숨 표시
        lives_text = FONT_SMALL.render(f"목숨: {self.lives}", True, WHITE)
        self.screen.blit(lives_text, (10, 40))

    def draw_game_over_screen(self):
        game_over_text = FONT_LARGE.render("게임 오버", True, PASTEL_PINK)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(game_over_text, game_over_rect)

        final_score_text = FONT_MEDIUM.render(f"최종 점수: {self.score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(final_score_text, final_score_rect)

        correct_list_text = FONT_SMALL.render("맞춘 사자성어:", True, PASTEL_YELLOW)
        correct_list_rect = correct_list_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(correct_list_text, correct_list_rect)
        
        # 맞춘 사자성어 목록을 화면 너비에 맞게 자동으로 줄바꿈하여 표시
        start_x = 50
        current_x = start_x
        current_y = correct_list_rect.bottom + 20
        for i, word in enumerate(self.correct_saja_list):
            word_text = FONT_SMALL.render(word, True, WHITE)
            word_rect = word_text.get_rect(topleft=(current_x, current_y))
            
            if word_rect.right > SCREEN_WIDTH - start_x:
                current_y += word_rect.height + 5
                current_x = start_x
                word_rect.topleft = (current_x, current_y)

            self.screen.blit(word_text, word_rect)
            current_x = word_rect.right + 15

        self.restart_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)
        pygame.draw.rect(self.screen, MINT, self.restart_button_rect)
        restart_text = FONT_MEDIUM.render("처음으로", True, WHITE)
        restart_text_rect = restart_text.get_rect(center=self.restart_button_rect.center)
        self.screen.blit(restart_text, restart_text_rect)
