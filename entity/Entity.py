import pygame as pg

class Entity(pg.sprite.Sprite):
    def __init__(self, image, position: pg.Vector2, size: int):
        super().__init__()
        self.image = image # 이미지 설정
        self.position = position # 위치 설정
        #self.image = pg.transform.scale(self.image, size)
        self.rect = self.image.get_rect() # 이미지 경계선(직사각형) / 히트박스
        self.rect.topleft = (self.position.x, self.position.y) 

        self.speed = 3 # 이동 속도
        self.direction = ""
        self.gravity_speed = 0 # 중력 속도
        self.gravity_acceleration = (0.05) # 중력 가속도
        self.jump_first_power = (7) # 점프 초기 힘
        self.jump_power = 0 # 점프 힘
        self.dropping = False

    def move(self, move: pg.Vector2):
        steps = [pg.Vector2(0, 0)]
        if move.x == 0:
            if move.y > 0:
                for i in range(1, int(move.y) + 1):
                    steps.append(pg.Vector2(0, int(i)))
            elif move.y < 0:
                for i in range(-1, int(move.y) - 1, -1):
                    steps.append(pg.Vector2(0, int(i)))
        elif move.x > 0:
            for i in range(1, int(move.x) + 1):
                steps.append(pg.Vector2(i, int(move.y * i) / move.x))
        else:
            for i in range(-1, int(move.x) - 1, -1):
                steps.append(pg.Vector2(i, int(move.y * i) / move.x))
                
        isCollide = False
        idx = len(steps) - 1
        for i in range(len(steps)):
            isCollide = self.isCollide(steps[i])
            if isCollide:
                idx = i - 1
                break

        self.rect.x += steps[idx].x
        self.rect.y += steps[idx].y
        self.position = self.rect.topleft

        return steps[idx]


    def isCollide(self, move: pg.Vector2): # 부딪치는지 여부 확인
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

    def gravity(self):
        self.gravity_speed += self.gravity_acceleration
        if self.gravity_speed < 1:
            return
        self.dropping = True
        move = self.move(pg.Vector2(0, int(self.gravity_speed)))
        if move.x == 0 and move.y == 0:
            self.dropping = False
            self.gravity_speed = 0

    def set_entity_list(self, entity_list):
        self.entity_list = entity_list

    def update(self): #미완성
        move_dest = pg.Vector2(0, 0)
        self.gravity()
        self.move(move_dest)
        # #self.rect.topleft = (int(self.position.x), int(self.position.y))
