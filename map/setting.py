import pygame as pg
from entity import Character
import os
import random
from block import Ground
import csv

screen_width, screen_height = None, None
screen = None
tile_size = None
TICK_PER_SECOND = None
player1 = None
player2 = None
players = None
objects = None

def createMap():
    global screen_width, screen_height, screen, tile_size, TICK_PER_SECOND, player1, player2, players, objects

    # 화면 크기 설정
    screen_width, screen_height = 1200, 900

    screen = pg.display.set_mode((screen_width, screen_height))

    tile_size = 10 # 타일 크기

    # 제목
    pg.display.set_caption("Fight PVP")

    # FPS 설정
    TICK_PER_SECOND = (50) # 초당 50틱 -> 1틱 = 0.02초

    #캐릭터 & 오브젝트
    RED = (255, 0, 0)
    BLUE = (0, 0, 225)
    players = pg.sprite.Group()
    objects = pg.sprite.Group()

    folder_path = os.path.join(os.path.dirname(__file__)+"/map_list")

    # 폴더 내 모든 파일 목록 가져오기
    file_list = os.listdir(folder_path)

    # 숨김 파일, 폴더 등 제외하고 파일만 필터링 (선택)
    file_list = [f for f in file_list if os.path.isfile(os.path.join(folder_path, f))]

    # 파일이 있을 때만 랜덤 선택
    if file_list:
        selected_file = random.choice(file_list)
        
        map_path = os.path.join(folder_path, selected_file)
        data = []

        with open(map_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)  # 각 행을 리스트로 추가

        for y in range(len(data)):
            for x in range(len(data[y])):
                if data[y][x] == 'P1':
                    player1 = Character(pg.Vector2(x*tile_size, y*tile_size), RED, 50, [pg.K_a, pg.K_d, pg.K_w])
                    players.add(player1)
                    objects.add(player1)
                elif data[y][x] == 'P2':
                    player2 = Character(pg.Vector2(x*tile_size, y*tile_size), BLUE,50, [pg.K_LEFT, pg.K_RIGHT, pg.K_UP])
                    players.add(player2)
                    objects.add(player2)
                elif data[y][x] == 'G':
                    ground = Ground(pg.Surface((tile_size, tile_size)), pg.Vector2(x * tile_size, y * tile_size))
                    objects.add(ground)
    else:
        print("폴더에 파일이 없습니다.")
