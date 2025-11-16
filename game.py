import pygame
import random
import time
import json  # [새로 추가] json 모듈 임포트
from settings import *
from player import Player
from enemy import Enemy
from bullet import Bullet
from heart import Heart


# --- 폭발 효과 클래스 (수정 없음) ---
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        try:
            self.image = pygame.image.load("img/Character_Death.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 40))
        except FileNotFoundError:
            print("경고: 'img/Character_Death.png' 파일을 찾을 수 없습니다. 주황색 원으로 대체합니다.")
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 100, 0), (20, 20), 20)

        self.rect = self.image.get_rect(center=center)
        self.spawn_time = pygame.time.get_ticks()
        self.duration = 200

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.spawn_time > self.duration:
            return False
        return True

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# ------------------------------------


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect()

        try:
            self.game_background_image = pygame.image.load("img/background.png").convert_alpha()
            self.game_background_image = pygame.transform.scale(self.game_background_image,
                                                                (SCREEN_WIDTH, SCREEN_HEIGHT))
        except FileNotFoundError:
            print("경고: 'img/background.png' 파일을 찾을 수 없습니다.")
            self.game_background_image = None

        # --- 시작 화면 이미지 로드 (수정 없음) ---
        self.logo_image = None
        self.start_button_image = None
        try:
            self.logo_image = pygame.image.load("img/logo.png").convert_alpha()
            logo_width = int(PLAY_AREA_RECT.width * 0.8)
            logo_height = int(self.logo_image.get_height() * (logo_width / self.logo_image.get_width()))
            self.logo_image = pygame.transform.scale(self.logo_image, (logo_width, logo_height))
        except FileNotFoundError:
            print("경고: 'img/logo.png' 파일을 찾을 수 없습니다.")

        try:
            self.start_button_image = pygame.image.load("img/startBtn.png").convert_alpha()
            btn_width = int(PLAY_AREA_RECT.width * 0.5)
            btn_height = int(self.start_button_image.get_height() * (btn_width / self.start_button_image.get_width()))
            self.start_button_image = pygame.transform.scale(self.start_button_image, (btn_width, btn_height))
        except FileNotFoundError:
            print("경고: 'img/startBtn.png' 파일을 찾을 수 없습니다.")

        if self.start_button_image:
            self.start_button_rect = self.start_button_image.get_rect(
                center=(PLAY_AREA_RECT.centerx, PLAY_AREA_RECT.centery + 80)
            )
        else:
            self.start_button_rect = pygame.Rect(0, 0, 150, 40)
            self.start_button_rect.center = (PLAY_AREA_RECT.centerx, PLAY_AREA_RECT.centery + 30)

        # --- 목숨(UI)용 하트 이미지 로드 (수정 없음) ---
        self.heart_ui_image = None
        try:
            self.heart_ui_image = pygame.image.load("img/heart.png").convert_alpha()
            self.heart_ui_image = pygame.transform.scale(self.heart_ui_image, (20, 20))  # UI용은 20x20
        except FileNotFoundError:
            print("경고: 'img/heart.png' (UI용) 파일을 찾을 수 없습니다. 텍스트로 대체합니다.")

        pygame.key.set_repeat(500, 30)
        pygame.display.set_caption("WordShot")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "START"

        # --- [수정] idioms.json 파일에서 사자성어 목록 불러오기 ---
        try:
            # 'utf-8' 인코딩을 명시하여 한글 파일 읽기
            with open('idioms.json', 'r', encoding='utf-8') as f:
                self.saja_list = json.load(f)

            # 파일은 있으나 내용이 비어있는 경우 예외 처리
            if not self.saja_list:
                print("경고: 'idioms.json' 파일이 비어있습니다. 기본 목록을 사용합니다.")
                raise FileNotFoundError  # 기본 목록을 사용하도록 예외 발생

            print(f"성공: 'idioms.json'에서 {len(self.saja_list)}개의 사자성어를 불러왔습니다.")

        except (FileNotFoundError, json.JSONDecodeError) as e:
            # 파일이 없거나, json 형식이 아닐 경우 (예: 비어있음)
            print(f"경고: 'idioms.json' 파일 로드 실패 ({e}). 기본 목록을 사용합니다.")
            # 예비용 기본 목록 (Fallback)
            self.saja_list = [
                {"word": "고진감래", "meaning": "고생 끝에 낙이 온다"},
                {"word": "동고동락", "meaning": "고통과 즐거움을 함께 한다"},
                {"word": "유비무환", "meaning": "미리 준비하면 근심이 없다"},
                {"word": "과유불급", "meaning": "지나친 것은 미치지 못한 것과 같다"},
                {"word": "다다익선", "meaning": "많으면 많을수록 좋다"},
                {"word": "일석이조", "meaning": "한 가지 일로 두 가지 이익을 얻음"},
                {"word": "자화자찬", "meaning": "자기가 한 일을 스스로 칭찬함"},
            ]
        # --- [수정 완료] ---

        self.player = Player(PLAY_AREA_RECT)
        self.reset_game_variables()

    def reset_game_variables(self):
        self.player.reset(PLAY_AREA_RECT)
        self.bullets = []
        self.enemies = []
        self.explosions = []
        self.hearts = []
        self.bullet_count = 0
        self.user_input = ""
        self.current_saja = random.choice(self.saja_list)
        self.score = 0
        self.correct_saja_list = []
        self.lives = 3
        self.last_enemy_spawn_time = time.time()
        self.enemy_spawn_interval = 4.0
        self.last_heart_spawn_time = time.time()
        self.heart_spawn_interval = random.uniform(10.0, 20.0)

        self.scroll_y = 0  # [새로 추가] 스크롤 Y 위치 변수

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    # --- [수정] handle_events ---
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
                # '처음으로' 버튼 클릭
                if hasattr(self,
                           'restart_button_rect') and event.type == pygame.MOUSEBUTTONDOWN and self.restart_button_rect.collidepoint(
                    event.pos):
                    self.game_state = "START"
                    pygame.key.stop_text_input()

                # [새로 추가] 마우스 휠 스크롤 감지
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # 휠 위로
                        self.scroll_y += 20  # 20픽셀씩 위로 (내용이 아래로)
                    elif event.button == 5:  # 휠 아래로
                        self.scroll_y -= 20  # 20픽셀씩 아래로 (내용이 위로)

                # [새로 추가] 스크롤 범위 제한 (0보다 위로 못 올라가게)
                if self.scroll_y > 0:
                    self.scroll_y = 0
                # (참고: 목록 맨 아래까지의 최대 스크롤 제한은 복잡해서 일단 생략했습니다)

    # ----------------------------

    def handle_playing_keydown(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.user_input = self.user_input[:-1]
        elif event.key == pygame.K_RETURN:
            if self.user_input == self.current_saja["word"]:
                player_pos = self.player.get_pos()
                self.bullets.append(Bullet(player_pos[0], player_pos[1]))

                # [수정 없음] 사자성어 딕셔너리 저장
                if self.current_saja not in self.correct_saja_list:
                    self.correct_saja_list.append(self.current_saja)

                new_saja = random.choice(self.saja_list)
                while new_saja == self.current_saja:
                    new_saja = random.choice(self.saja_list)
                self.current_saja = new_saja
            self.user_input = ""

    def update(self):
        if self.game_state != "PLAYING":
            return

        # (이하 update 로직은 수정 없음)
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
            self.enemy_spawn_interval = max(self.enemy_spawn_interval, 1.0)

        if current_time - self.last_heart_spawn_time > self.heart_spawn_interval:
            self.hearts.append(Heart(PLAY_AREA_RECT))
            self.last_heart_spawn_time = current_time
            self.heart_spawn_interval = random.uniform(10.0, 20.0)

        for enemy in self.enemies:
            enemy.update()
            if enemy.rect.top > PLAY_AREA_RECT.bottom:
                self.enemies.remove(enemy)
                self.lives -= 1

        for heart in self.hearts[::]:
            heart.update()
            if heart.rect.top > PLAY_AREA_RECT.bottom:
                self.hearts.remove(heart)

        if self.lives <= 0:
            self.game_state = "GAME_OVER"
            pygame.key.stop_text_input()

        bullets_to_remove = []
        enemies_to_remove = []
        hearts_to_remove = []

        for bullet in self.bullets:
            if bullet in bullets_to_remove: continue
            for heart in self.hearts:
                if heart in hearts_to_remove: continue
                if bullet.rect.colliderect(heart.rect):
                    bullets_to_remove.append(bullet)
                    hearts_to_remove.append(heart)
                    if self.lives < 3:
                        self.lives += 1
                    break

        for bullet in self.bullets:
            if bullet in bullets_to_remove: continue
            for enemy in self.enemies:
                if enemy in enemies_to_remove: continue
                if bullet.rect.colliderect(enemy.rect.inflate(10, 10)):
                    bullets_to_remove.append(bullet)
                    enemies_to_remove.append(enemy)
                    self.explosions.append(Explosion(enemy.rect.center))
                    self.score += 10
                    break

        for bullet in list(set(bullets_to_remove)):
            self.bullets.remove(bullet)
        for heart in list(set(hearts_to_remove)):
            self.hearts.remove(heart)
        for enemy in list(set(enemies_to_remove)):
            self.enemies.remove(enemy)

        for explosion in self.explosions[::]:
            if not explosion.update():
                self.explosions.remove(explosion)

    def draw_main_ui(self):
        score_text = FONT_GUI.render(f"{self.score}", True, DEEP_PINK)
        score_rect = score_text.get_rect(center=SCORE_POS)
        self.screen.blit(score_text, score_rect)

        if self.heart_ui_image:
            start_x = LIVES_POS[0]
            start_y = LIVES_POS[1]
            heart_width = self.heart_ui_image.get_width()
            heart_padding = 5

            for i in range(self.lives):
                x_pos = start_x + (i * (heart_width + heart_padding))
                y_pos = start_y - self.heart_ui_image.get_height() // 2
                self.screen.blit(self.heart_ui_image, (x_pos, y_pos))
        else:
            lives_text = FONT_GUI.render(f"LIVES: {self.lives}", True, DEEP_PINK)
            lives_rect = lives_text.get_rect(center=LIVES_POS)
            self.screen.blit(lives_text, lives_rect)

    def draw(self):
        self.screen.fill(BLACK)
        if self.game_background_image:
            self.screen.blit(self.game_background_image, (0, 0))
        else:
            pygame.draw.rect(self.screen, BLACK, PLAY_AREA_RECT)

        if self.game_state == "START":
            self.draw_start_screen()

        elif self.game_state == "PLAYING":
            self.draw_playing_screen()
            self.draw_main_ui()

        elif self.game_state == "GAME_OVER":
            self.draw_game_over_screen()
            self.draw_main_ui()

        pygame.display.flip()

    def draw_start_screen(self):
        if self.logo_image:
            logo_rect = self.logo_image.get_rect(center=(PLAY_AREA_RECT.centerx, PLAY_AREA_RECT.centery - 40))
            self.screen.blit(self.logo_image, logo_rect)
        else:
            title_text = FONT_LARGE.render("WordShot", True, DEEP_PINK)
            title_rect = title_text.get_rect(center=(PLAY_AREA_RECT.centerx, PLAY_AREA_RECT.centery - 40))
            self.screen.blit(title_text, title_rect)

        if self.start_button_image:
            self.screen.blit(self.start_button_image, self.start_button_rect)
        else:
            pygame.draw.rect(self.screen, MINT, self.start_button_rect)
            start_text = FONT_MEDIUM.render("Start", True, DEEP_PINK)
            start_text_rect = start_text.get_rect(center=self.start_button_rect.center)
            self.screen.blit(start_text, start_text_rect)

    def draw_playing_screen(self):
        self.player.draw(self.screen)
        for bullet in self.bullets:
            if bullet.rect.colliderect(PLAY_AREA_RECT):
                bullet.draw(self.screen)
        for enemy in self.enemies:
            if enemy.rect.colliderect(PLAY_AREA_RECT):
                enemy.draw(self.screen)
        for heart in self.hearts:
            if heart.rect.colliderect(PLAY_AREA_RECT):
                heart.draw(self.screen)
        for explosion in self.explosions:
            explosion.draw(self.screen)

        saja_text = FONT_MEDIUM.render(self.current_saja['word'], True, DEEP_PINK)
        saja_rect = saja_text.get_rect(center=SAJA_WORD_POS)
        self.screen.blit(saja_text, saja_rect)

        meaning_text = FONT_SMALL.render(self.current_saja['meaning'], True, MEDIUM_GRAY)
        meaning_rect = meaning_text.get_rect(center=SAJA_MEANING_POS)
        self.screen.blit(meaning_text, meaning_rect)

        input_text = FONT_MEDIUM.render(self.user_input, True, MUSTARD)
        underline_width = max(100, input_text.get_width() + 10)
        underline_pos_start = (UI_CENTER_X - underline_width // 2, INPUT_BOX_Y + 5)
        underline_pos_end = (UI_CENTER_X + underline_width // 2, INPUT_BOX_Y + 5)
        pygame.draw.line(self.screen, MUSTARD, underline_pos_start, underline_pos_end, 2)
        input_rect = input_text.get_rect(midbottom=(UI_CENTER_X, INPUT_BOX_Y))
        self.screen.blit(input_text, input_rect)

    # --- [수정] draw_game_over_screen ---
    def draw_game_over_screen(self):
        # 1. "게임 오버", "최종 점수", "맞춘 사자성어" 타이틀 그리기 (수정 없음)
        game_over_text = FONT_LARGE.render("게임 오버", True, PASTEL_PINK)
        game_over_rect = game_over_text.get_rect(center=(PLAY_AREA_RECT.centerx, PLAY_AREA_RECT.top + 40))
        self.screen.blit(game_over_text, game_over_rect)

        final_score_text = FONT_MEDIUM.render(f"최종 점수: {self.score}", True, DEEP_PINK)
        final_score_rect = final_score_text.get_rect(center=(PLAY_AREA_RECT.centerx, game_over_rect.bottom + 30))
        self.screen.blit(final_score_text, final_score_rect)

        correct_list_text = FONT_SMALL.render("맞춘 사자성어:", True, PASTEL_YELLOW)
        correct_list_rect = correct_list_text.get_rect(center=(PLAY_AREA_RECT.centerx, final_score_rect.bottom + 30))
        self.screen.blit(correct_list_text, correct_list_rect)

        # 2. [새로 추가] '처음으로' 버튼 Rect 먼저 정의 (스크롤 영역 계산용)
        self.restart_button_rect = pygame.Rect(0, 0, 150, 40)
        self.restart_button_rect.center = (PLAY_AREA_RECT.centerx, PLAY_AREA_RECT.bottom - 25)

        # 3. [새로 추가] 스크롤 목록이 그려질 영역(clip_rect) 정의
        # "맞춘 사자성어" 텍스트 10픽셀 아래부터
        list_area_top = correct_list_rect.bottom + 10
        # '처음으로' 버튼 10픽셀 위까지
        list_area_bottom = self.restart_button_rect.top - 10
        # Rect(x, y, width, height)
        clip_rect = pygame.Rect(
            PLAY_AREA_RECT.left, list_area_top,
            PLAY_AREA_RECT.width, list_area_bottom - list_area_top
        )

        # 4. [새로 추가] 화면 잘라내기(clipping) 설정
        # 이 코드 이후 .blit()은 clip_rect 안쪽에만 그려집니다.
        self.screen.set_clip(clip_rect)

        # --- [수정] 맞춘 사자성어 목록 (스크롤 적용) ---

        start_x = PLAY_AREA_RECT.left + 10
        # [수정] current_y가 스크롤 위치(self.scroll_y)를 반영하도록
        current_y = list_area_top + self.scroll_y
        max_width = PLAY_AREA_RECT.width - 20

        padding_between_lines = 2
        padding_between_entries = 5

        for saja_dict in self.correct_saja_list:

            # (이하 그리기 로직은 수정 없음)
            # 1. 단어 그리기 (DEEP_PINK)
            word_text = FONT_SMALL.render(saja_dict['word'], True, DEEP_PINK)
            word_rect = word_text.get_rect(topleft=(start_x, current_y))
            self.screen.blit(word_text, word_rect)
            current_y = word_rect.bottom + padding_between_lines

            # 2. 뜻 그리기 (MEDIUM_GRAY) - 텍스트 자동 줄바꿈
            words = saja_dict['meaning'].split(' ')
            line = ""
            for word in words:
                test_line = line + word + " "
                test_text = FONT_SMALL.render(test_line, True, MEDIUM_GRAY)
                if test_text.get_width() > max_width:
                    line_text = FONT_SMALL.render(line, True, MEDIUM_GRAY)
                    self.screen.blit(line_text, (start_x, current_y))
                    current_y += line_text.get_height()
                    line = word + " "
                else:
                    line = test_line

            line_text = FONT_SMALL.render(line, True, MEDIUM_GRAY)
            self.screen.blit(line_text, (start_x, current_y))
            current_y += line_text.get_height()
            current_y += padding_between_entries

            # [삭제] Y좌표가 버튼을 침범하는지 검사하는 'break'문 삭제
            # (clipping 영역이 자동으로 잘라주므로 필요 없음)

        # 5. [새로 추가] 화면 잘라내기(clipping) 해제
        # 이 코드 이후 .blit()은 다시 화면 전체에 그려집니다.
        self.screen.set_clip(None)

        # 6. '처음으로' 버튼 그리기 (clipping 해제 후)
        pygame.draw.rect(self.screen, MINT, self.restart_button_rect)
        restart_text = FONT_MEDIUM.render("처음으로", True, DEEP_PINK)
        restart_text_rect = restart_text.get_rect(center=self.restart_button_rect.center)
        self.screen.blit(restart_text, restart_text_rect)