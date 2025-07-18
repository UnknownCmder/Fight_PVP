import pygame

# 화면 크기 설정
screen_width, screen_height = 1200, 900
screen = pygame.display.set_mode((screen_width, screen_height))
tile_size = 10 # 타일 크기

# 제목
pygame.display.set_caption("Pygame 기본 템플릿")

# FPS 설정
TICK_PER_SECOND = (50) # 초당 50틱 -> 1틱 = 0.02초

#맵 파일은 .csv