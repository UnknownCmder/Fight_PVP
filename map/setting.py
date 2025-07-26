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
background_image = (255, 255, 255)  # 흰색 배경

def createMap():
    global screen_width, screen_height, screen, tile_size, TICK_PER_SECOND, player1, player2, players, objects

    screen_width, screen_height = 1200, 900 # 화면 크기 설정
    screen = pg.display.set_mode((screen_width, screen_height)) # 화면 생성
    tile_size = 10 # 타일 크기
    pg.display.set_caption("Fight PVP") # 게임 제목 설정

    # FPS 설정
    TICK_PER_SECOND = (50) # 초당 50틱 -> 1틱 = 0.02초

    #캐릭터 & 오브젝트
    RED = (255, 0, 0) #임시 플레이어 색상 (추후 삭제)
    BLUE = (0, 0, 225) #임시 플레이어 색상 (추후 삭제)
    players = pg.sprite.Group() # 플레이어 그룹
    objects = pg.sprite.Group() # 오브젝트 그룹

    folder_path = os.path.join(os.path.dirname(__file__)+"/map_list")
    file_list = os.listdir(folder_path) # 폴더 내 모든 파일 목록 가져오기
    file_list = [f for f in file_list if os.path.isfile(os.path.join(folder_path, f))] # 숨김 파일, 폴더 등 제외하고 파일만 필터링

    # 파일이 있을 때만 랜덤 선택
    if file_list:
        selected_file = random.choice(file_list) # 랜덤으로 파일 선택
        map_path = os.path.join(folder_path, selected_file) # 선택된 맵 파일 경로
        data = [] # 맵 데이터 초기화

        with open(map_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)  # 각 행을 리스트로 추가

        # 맵 생성
        for y in range(len(data)):
            for x in range(len(data[y])):
                if data[y][x] == 'P1':
                    #임시로 플레이어 이미지 생성 (추후에 삭제)
                    image = pg.Surface((100, 100))
                    image.fill(RED)
                    
                    player1 = Character(image, pg.Vector2(x*tile_size, y*tile_size), 50, [pg.K_a, pg.K_d, pg.K_w])
                    players.add(player1)
                    objects.add(player1)
                elif data[y][x] == 'P2':
                    #임시로 플레이어 이미지 생성 (추후에 삭제)
                    image = pg.Surface((100, 100))
                    image.fill(BLUE)

                    player2 = Character(image, pg.Vector2(x*tile_size, y*tile_size),50, [pg.K_LEFT, pg.K_RIGHT, pg.K_UP])
                    players.add(player2)
                    objects.add(player2)
                elif data[y][x] == 'G':
                    # 임시로 바닥 이미지 생성 (추후에 삭제)
                    image = pg.Surface((tile_size, tile_size))
                    image.fill((0, 255, 0))  # 녹색으로 채우기
                    
                    ground = Ground(image, pg.Vector2(x * tile_size, y * tile_size))
                    objects.add(ground)
    else:
        print("폴더에 맵이 없습니다")
