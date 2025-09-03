tile_size = 30 # 타일 크기
#screen_width, screen_height = 1200, 900
screen_width, screen_height = tile_size * 40, tile_size * 30 # 화면 크기

# FPS 설정
TICK_PER_SECOND = (50) # 초당 50틱 -> 1틱 = 0.02초

screen = None

def init_setting():
    global screen
    import pygame as pg
    pg.init()
    screen = pg.display.set_mode((screen_width, screen_height)) # 화면 생성
    pg.display.set_caption("Fight PVP") # 게임 제목 설정