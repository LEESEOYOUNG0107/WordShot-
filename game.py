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
        self.last_enemy_spawn_time = time.time()
        self.enemy_spawn_interval = 2.0

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
            elif self.game_state == "START":
                if event.type == pygame.MOUSEBUTTONDOWN and self.start_button_rect.collidepoint(event.pos):
                    self.reset_game_variables()
                    self.game_state = "PLAYING"
            elif self.game_state == "GAME_OVER":
                if event.type == pygame.MOUSEBUTTONDOWN and self.restart_button_rect.collidepoint(event.pos):
                    self.game_state = "START"

    def handle_playing_keydown(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.user_input = self.user_input[:-1]
        elif event.key == pygame.K_RETURN:
            if self.user_input == self.current_saja["word"]:
                self.bullet_count += 1
                if self.current_saja["word"] not in self.correct_saja_list:
                    self.correct_saja_list.append(self.current_saja["word"])
                
                new_saja = random.choice(self.saja_list)
                while new_saja == self.current_saja:
                    new_saja = random.choice(self.saja_list)
                self.current_saja = new_saja
            self.user_input = ""
        elif event.key == pygame.K_SPACE:
            if self.bullet_count > 0:
                player_pos = self.player.get_pos()
                self.bullets.append(Bullet(player_pos[0], player_pos[1]))
                self.bullet_count -= 1
        else:
            self.user_input += event.unicode

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
            if self.enemy_spawn_interval > 0.5:
                self.enemy_spawn_interval *= 0.99

        for enemy in self.enemies:
            enemy.update()
            if enemy.rect.top > SCREEN_HEIGHT:
                self.enemies.remove(enemy)
                self.game_state = "GAME_OVER"

        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    break

    def draw(self):
        self.screen.fill(BLACK)
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
        pygame.draw.rect(self.screen, BLUE, self.start_button_rect)
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
        
        saja_text = FONT_MEDIUM.render(f"{self.current_saja['word']} ({self.current_saja['meaning']})", True, WHITE)
        saja_rect = saja_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 25))
        self.screen.blit(saja_text, saja_rect)

        input_text = FONT_MEDIUM.render(self.user_input, True, YELLOW)
        input_rect = input_text.get_rect(midleft=(10, SCREEN_HEIGHT // 2))
        self.screen.blit(input_text, input_rect)

        score_text = FONT_SMALL.render(f"점수: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        bullet_text = FONT_SMALL.render(f"총알: {self.bullet_count}", True, YELLOW)
        bullet_text_rect = bullet_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        self.screen.blit(bullet_text, bullet_text_rect)

    def draw_game_over_screen(self):
        game_over_text = FONT_LARGE.render("게임 오버", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(game_over_text, game_over_rect)

        final_score_text = FONT_MEDIUM.render(f"최종 점수: {self.score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(final_score_text, final_score_rect)

        correct_list_text = FONT_SMALL.render("맞춘 사자성어:", True, YELLOW)
        correct_list_rect = correct_list_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(correct_list_text, correct_list_rect)
        
        for i, word in enumerate(self.correct_saja_list):
            line = i // 5
            pos = i % 5
            word_text = FONT_SMALL.render(word, True, WHITE)
            word_rect = word_text.get_rect(center=(SCREEN_WIDTH // 2 - 160 + (pos * 80), SCREEN_HEIGHT // 2 + 60 + (line * 30)))
            self.screen.blit(word_text, word_rect)

        self.restart_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)
        pygame.draw.rect(self.screen, BLUE, self.restart_button_rect)
        restart_text = FONT_MEDIUM.render("처음으로", True, WHITE)
        restart_text_rect = restart_text.get_rect(center=self.restart_button_rect.center)
        self.screen.blit(restart_text, restart_text_rect)