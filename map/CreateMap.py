import pygame as pg
from entity import Character
import os
import random
from block import Ground
import csv

player1 = None
player2 = None
players = None
grounds = None
guns = None
bullets = None
WHITE = (255, 255, 255)  # 흰색 배경
background_image = None

def createMap():
    from .init_setting import tile_size, screen, screen_width, screen_height
    from Select_map import selected_map
    global player1, player2, players, guns, grounds, bullets, WHITE, background_image

    screen.fill(WHITE) # 배경화면 그리기 (나중에는 이미지 삽입으로 변경)
    background_image = pg.image.load("./assets/ingame_background.png").convert() # 배경 이미지 불러오기
    screen.blit(background_image, (0, 0)) # 배경화면 그리기 (나중에는 이미지 삽입으로 변경)

    #캐릭터 & 오브젝트
    RED = (255, 0, 0) #임시 플레이어 색상 (추후 삭제)
    BLUE = (0, 0, 225) #임시 플레이어 색상 (추후 삭제)
    players = pg.sprite.Group() # 플레이어 그룹
    grounds = pg.sprite.Group() # 바닥 그룹

    file_list = None
    folder_path = os.path.join(os.path.dirname(__file__)+"/map_list")
    if selected_map == "RANDOM":
        file_list = os.listdir(folder_path) # 폴더 내 모든 파일 목록 가져오기
        file_list = [f for f in file_list if os.path.isfile(os.path.join(folder_path, f))] # 숨김 파일, 폴더 등 제외하고 파일만 필터링
    else:
        file_list = [os.path.join(folder_path, selected_map)] # 선택된 맵 파일만 리스트에 추가

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
                    image = pg.image.load("./assets/player1.png").convert_alpha()
                    
                    player1 = Character(1, image, pg.Vector2(x*tile_size, y*tile_size), 50, [pg.K_a, pg.K_d, pg.K_w, pg.K_s])
                elif data[y][x] == 'P2':
                    image = pg.image.load("./assets/player2.png").convert_alpha()

                    player2 = Character(2, image, pg.Vector2(x*tile_size, y*tile_size), 50, [pg.K_j, pg.K_l, pg.K_i, pg.K_k])
                elif data[y][x] == 'Gm':
                    # 임시로 바닥 이미지 생성 (추후에 삭제)
                    image = pg.image.load("./assets/mid_ground.png").convert_alpha()
                    
                    ground = Ground(image, pg.Vector2(x * tile_size, y * tile_size), tile_size)
                    grounds.add(ground)
                elif data[y][x] == 'Gl':
                    image = pg.image.load("./assets/left_ground.png").convert_alpha()
                    
                    ground = Ground(image, pg.Vector2(x * tile_size, y * tile_size), tile_size)
                    grounds.add(ground)
                elif data[y][x] == 'Gr':
                    image = pg.image.load("./assets/right_ground.png").convert_alpha()
                    
                    ground = Ground(image, pg.Vector2(x * tile_size, y * tile_size), tile_size)
                    grounds.add(ground)

        # 플레이어 총 생성
        image = pg.image.load("./assets/right_gun.png").convert_alpha()
        image = pg.transform.rotate(image, -90)
        player1.getGun(image, 80, 20)  # 플레이어 총 생성 (임시 이미지 사용)
        
        image = pg.image.load("./assets/left_gun.png").convert_alpha()
        image = pg.transform.rotate(image, 90)
        player2.getGun(image, 80, 20)  # 플레이어 총 생성 (임시 이미지 사용)
        players.add(player1, player2)

        guns = pg.sprite.Group()  # 총 그룹 생성
        guns.add(player1.gun, player2.gun)  # 총을 그룹에 추가
        
        bullets = pg.sprite.Group()  # 총알 그룹 생성
    else:
        print("폴더에 맵이 없습니다")
