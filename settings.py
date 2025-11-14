import pygame

# 화면 설정
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 700

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 파스텔톤 색상
PASTEL_PINK = (255, 204, 204) # 적
PASTEL_YELLOW = (255, 255, 204) # 총알
PASTEL_BLUE = (173, 216, 230) # 플레이어
MINT = (189, 252, 201) # 버튼

BG_COLOR = (10, 20, 40) # 어두운 남색 배경

# --- 폰트 자동 찾기 설정 ---
pygame.init()

def find_font():
    """'font' 폴더에서 .ttf 또는 .otf 폰트 파일을 자동으로 찾습니다."""
    import os
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
        raise FileNotFoundError # 폰트 파일이 없으면 에러 발생
    FONT_LARGE = pygame.font.Font(FONT_PATH, 72)
    FONT_MEDIUM = pygame.font.Font(FONT_PATH, 36)
    FONT_SMALL = pygame.font.Font(FONT_PATH, 24)
    print(f"폰트 불러오기 성공: {FONT_PATH}")
except FileNotFoundError:
    print(f"경고: 'font' 폴더에 폰트 파일(.ttf, .otf)이 없습니다. 기본 폰트를 사용합니다 (한글 깨짐 발생).")
    FONT_LARGE = pygame.font.Font(None, 72)
    FONT_MEDIUM = pygame.font.Font(None, 36)
    FONT_SMALL = pygame.font.Font(None, 24)