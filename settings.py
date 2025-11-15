import pygame
import os

# 게임 윈도우 전체 크기 (수정 X)
SCREEN_WIDTH = 375
SCREEN_HEIGHT = 666

# -----------------------------------------------------------------
# 실제 게임 화면 영역 (사용자 지정값)
PLAY_AREA_RECT = pygame.Rect(82, 111, 241, 329)
# -----------------------------------------------------------------

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 파스텔톤 색상
PASTEL_PINK = (255, 204, 204)  # 적
PASTEL_YELLOW = (255, 255, 204)  # 총알
PASTEL_BLUE = (173, 216, 230)  # 플레이어
MINT = (189, 252, 201)  # 버튼

# --- [수정] UI 위치 정의 (PLAY_AREA_RECT 기준) ---

# 점수 (게임 영역 우측 상단)
SCORE_POS = (PLAY_AREA_RECT.right - 30, PLAY_AREA_RECT.top + 15)
# 목숨 (게임 영역 좌측 상단)
LIVES_POS = (PLAY_AREA_RECT.left + 35, PLAY_AREA_RECT.top + 15)

# 하단 입력창 및 사자성어 위치 (게임 영역 하단 기준)
# Y 위치
INPUT_BOX_Y = PLAY_AREA_RECT.bottom - 20  # 입력창 Y
SAJA_WORD_Y = PLAY_AREA_RECT.bottom - 45  # 사자성어 Y
SAJA_MEANING_Y = PLAY_AREA_RECT.bottom - 65  # 사자성어 뜻 Y
# X 위치 (게임 영역 중앙)
UI_CENTER_X = PLAY_AREA_RECT.centerx

# (X, Y) 튜플로 최종 정의
SAJA_MEANING_POS = (UI_CENTER_X, SAJA_MEANING_Y)
SAJA_WORD_POS = (UI_CENTER_X, SAJA_WORD_Y)

# --- [수정] 폰트 설정 (게임 영역이 좁으므로 크기 대폭 축소) ---
pygame.init()


def find_font():
    """'font' 폴더에서 .ttf 또는 .otf 폰트 파일을 자동으로 찾습니다."""
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
    # [수정] 폰트 크기 줄임
    FONT_LARGE = pygame.font.Font(FONT_PATH, 30)  # 60 -> 30
    FONT_MEDIUM = pygame.font.Font(FONT_PATH, 18)  # 30 -> 18
    FONT_SMALL = pygame.font.Font(FONT_PATH, 14)  # 22 -> 14
    FONT_GUI = pygame.font.Font(FONT_PATH, 15)  # 24 -> 15 (점수/목숨)
    print(f"폰트 불러오기 성공: {FONT_PATH}")
except FileNotFoundError:
    print(f"경고: 'font' 폴더에 폰트 파일(.ttf, .otf)이 없습니다. 기본 폰트를 사용합니다.")
    # [수정] 기본 폰트 크기도 줄임
    FONT_LARGE = pygame.font.Font(None, 30)
    FONT_MEDIUM = pygame.font.Font(None, 18)
    FONT_SMALL = pygame.font.Font(None, 14)
    FONT_GUI = pygame.font.Font(None, 15)