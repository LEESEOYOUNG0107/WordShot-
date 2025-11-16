import pygame
import os

# 게임 윈도우 전체 크기 (수정 X)
SCREEN_WIDTH = 375
SCREEN_HEIGHT = 666

# 실제 게임 화면 영역 (수정 X)
PLAY_AREA_RECT = pygame.Rect(82, 111, 241, 329)

# 색상 정의 (수정 X)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DEEP_PINK = (200, 80, 120)  # 사자성어(단어)용
MEDIUM_GRAY = (100, 100, 100)  # 사자성어(뜻)용
MUSTARD = (220, 180, 0)  # 사용자 입력용 (진한 노랑)
PASTEL_PINK = (255, 204, 204)  # 적
PASTEL_YELLOW = (255, 255, 204)  # 총알
PASTEL_BLUE = (173, 216, 230)  # 플레이어
MINT = (189, 252, 201)  # 버튼

# --- [수정] UI 위치 정의 (10px씩 아래로) ---

# [유지] 점수 (게임 영역 좌측 상단)
SCORE_POS = (PLAY_AREA_RECT.left + 20, PLAY_AREA_RECT.top + 15)
# [유지] 목숨 (게임 영역 우측 상단)
LIVES_POS = (PLAY_AREA_RECT.right - 80, PLAY_AREA_RECT.top + 15)

# [수정] 하단 입력창 및 사자성어 위치 (10px 아래로)
# Y 위치
INPUT_BOX_Y = PLAY_AREA_RECT.bottom - 30  # 입력창 Y (40 -> 30)
SAJA_MEANING_Y = PLAY_AREA_RECT.bottom - 55  # 사자성어 뜻 Y (65 -> 55)
SAJA_WORD_Y = PLAY_AREA_RECT.bottom - 75  # 사자성어 단어 Y (85 -> 75)
# X 위치 (게임 영역 중앙)
UI_CENTER_X = PLAY_AREA_RECT.centerx

# (X, Y) 튜플로 최종 정의
SAJA_MEANING_POS = (UI_CENTER_X, SAJA_MEANING_Y)
SAJA_WORD_POS = (UI_CENTER_X, SAJA_WORD_Y)

# --- 폰트 설정 (수정 없음) ---
pygame.init()


def find_font():
    font_dir = 'font'
    if not os.path.exists(font_dir):
        return None
    for filename in os.listdir(font_dir):
        if filename.lower().endswith(('.ttf', '.otf')):
            return os.path.join(font_dir, filename)
    return None


FONT_PATH = find_font()

try:
    if FONT_PATH is None:
        raise FileNotFoundError

    FONT_LARGE = pygame.font.Font(FONT_PATH, 30)
    FONT_MEDIUM = pygame.font.Font(FONT_PATH, 18)
    FONT_SMALL = pygame.font.Font(FONT_PATH, 14)
    FONT_GUI = pygame.font.Font(FONT_PATH, 15)

    print(f"폰트 불러오기 성공: {FONT_PATH}")
except FileNotFoundError:
    print(f"경고: 'font' 폴더에 폰트 파일(.ttf, .otf)이 없습니다. 기본 폰트를 사용합니다.")

    FONT_LARGE = pygame.font.Font(None, 30)
    FONT_MEDIUM = pygame.font.Font(None, 18)
    FONT_SMALL = pygame.font.Font(None, 14)
    FONT_GUI = pygame.font.Font(None, 15)