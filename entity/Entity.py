import pygame as pg

class Entity(pg.sprite.Sprite):
    def __init__(self, image, position: pg.Vector2, size: int):
        super().__init__()
        self.image = image # 이미지 설정
        self.image = pg.transform.scale(self.image, size) # 이미지 크기 조정
        self.position = position # 위치 설정

        self.rect = self.image.get_rect() # 히트박스(직사각형)
        self.rect.topleft = (self.position.x, self.position.y) # 직사각형 위치 설정

        self.speed = 3 # 이동 속도
        self.gravity_speed = 0 # 중력 속도
        self.gravity_acceleration = (0.05) # 중력 가속도
        self.jump_first_power = (7) # 점프 초기 힘
        self.jump_power = 0 # 점프 힘
        self.dropping = False # 낙하 중인지 여부
        
    def move(self, move: pg.Vector2):
        steps = [pg.Vector2(0, 0)]  # 시작 위치(0,0)를 steps 리스트에 추가
        if move.x == 0: # x축 이동이 없을 때 (수직 이동)
            if move.y > 0:
                # y가 양수면 위쪽으로 한 칸씩 이동 경로 추가
                for i in range(1, int(move.y) + 1):
                    steps.append(pg.Vector2(0, int(i)))
            elif move.y < 0:
                # y가 음수면 아래쪽으로 한 칸씩 이동 경로 추가
                for i in range(-1, int(move.y) - 1, -1):
                    steps.append(pg.Vector2(0, int(i)))
        elif move.x > 0: # x축 이동이 양수일 때 (오른쪽 대각선 또는 수평 이동)
            for i in range(1, int(move.x) + 1):
                steps.append(pg.Vector2(i, int(move.y * i) / move.x)) # y는 기울기 이용
        else: # x축 이동이 음수일 때 (왼쪽 대각선 또는 수평 이동)
            for i in range(-1, int(move.x) - 1, -1):
                steps.append(pg.Vector2(i, int(move.y * i) / move.x)) #y는 기울기 이용
                
        # 충돌 체크
        idx = len(steps) - 1
        for i in range(len(steps)):
            if self.isCollide(steps[i]):
                idx = i - 1
                break

        # 이동
        self.rect.x += steps[idx].x
        self.rect.y += steps[idx].y
        self.position = self.rect.topleft

        return steps[idx] # 이동한 거리 반환


    def isCollide(self, move: pg.Vector2): # 충돌 여부 확인
        # 충돌 여부를 확인하기 위해 임시로 rect를 복사
        temp_rect = self.rect.copy()
        temp_rect.x += int(move.x)
        temp_rect.y += int(move.y)

        from map.setting import screen_width, screen_height, objects
        if temp_rect.left < 0 or temp_rect.right > screen_width or temp_rect.top < 0 or temp_rect.bottom > screen_height: # 화면 밖으로 나가는지 확인
            return True
        
        for obj in objects: #충돌 체크
            if obj != self and temp_rect.colliderect(obj.rect):
                return True
            
        return False

    def gravity(self): # 중력 적용
        self.gravity_speed += self.gravity_acceleration # 중력 가속도 적용
        if self.gravity_speed < 1: # 중력 속도가 1보다 작으면 중력 적용 안함 (떨어진 거리(move)가 (0, 0)이라서 땅에 닿았다고 판단되어 중력 속도가 초기화됨)
            return
        
        self.dropping = True # 낙하 중으로 설정
        move = self.move(pg.Vector2(0, int(self.gravity_speed))) # 떨어진 거리
        if move.y == 0: # 땅에 닿았을 때
            # 중력 속도 초기화
            self.gravity_speed = 0
            self.dropping = False

    def update(self):
        # 이동
        self.gravity()
