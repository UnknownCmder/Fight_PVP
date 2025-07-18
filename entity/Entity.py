import pygame as pg
from map import screen_width, screen_height

class Entity(pg.sprite.Sprite):
    def __init__(self, image, position: pg.Vector2, size: int):
        super().__init__()
        self.image = image # 이미지 설정
        self.position = position # 위치 설정
        #self.image = pg.transform.scale(self.image, size)
        self.rect = self.image.get_rect() # 이미지 경계선(직사각형) / 히트박스
        self.rect.topleft = (self.position.x, self.position.y) 

        self.speed = 5 # 이동 속도
        self.direction = ""
        self.gravity_speed = 0 # 중력 속도
        self.gravity_acceleration = (0.3) # 중력 가속도
        self.jump_first_power = (15) # 점프 초기 힘
        self.jump_power = 0 # 점프 힘

        self.test = pg.Vector2(0, 0) # 테스트용 벡터

    def move(self, vector: pg.Vector2):
        inclination = pg.Vector2(0, 0) # 충동 확인을 위한 벡터
        if (vector.x == 0):
            if vector.y > 0:
                inclination = pg.Vector2(0, -1)
            elif (vector.y < 0):
                inclination = pg.Vector2(0, 1)
        elif vector.y == 0:
            if vector.x > 0:
                inclination = pg.Vector2(-1, 0)
            elif vector.x < 0:
                inclination = pg.Vector2(1, 0)
        else:
            inclination = pg.Vector2(1, vector.y / vector.x) #충동 확인을 위해 다시 돌아갈 때 x 1당 y가 얼마나 움직이는지지

        if (vector.x > 0 and vector.y < 0) or (vector.x > 0 and vector.y > 0):
            inclination.x *= -1
            inclination.y *= -1
        elif (vector.x < 0 and vector.y > 0):
            pass
        elif (vector.x < 0 and vector.y < 0):
            pass

        #test
        if (self.test != inclination):
            print("inclination :", inclination)
        self.test = inclination

        new_pos = self.position + vector
        
        count = 0 # 무한루프 방지용 카운트
        print("wfewfwefwefwfwfwe")
        while True:
            print("new_pos :", new_pos)
            if count > 100: # 무한루프 방지
                print("무한루프 방지")
                break
            if self.isCollide(new_pos):
                new_pos += inclination # 충돌 시 이동 방향을 반대로
            else:
                self.position = pg.Vector2(int(new_pos.x), int(new_pos.y)) # 충돌하지 않으면 위치 업데이트
                self.rect.topleft = (self.position.x, self.position.y)
                break
            count += 1
    
    def isCollide(self, vector: pg.Vector2): # 부딪치는지 여부 확인
        temp_rect = self.rect.copy()
        temp_rect.x = int(vector.x)
        temp_rect.y = int(vector.y)

        if temp_rect.left < 0 or temp_rect.right > screen_width or temp_rect.top < 0 or temp_rect.bottom > screen_height: # 화면 밖으로 나가는지 확인
            return True
        
        import entity.Entity_list as EntityList
        for entity in EntityList.entity_list: # 엔티티 리스트에서 충돌 체크
            if temp_rect.colliderect(entity.rect) and entity != self:
                return True
            
        return False

    def gravity(self):
        self.gravity_speed += self.gravity_acceleration
        if self.isCollide(pg.Vector2(self.position.x, self.position.y + int(self.gravity_speed))):
            self.gravity_speed = 0
        return pg.Vector2(0, int(self.gravity_speed))

    def set_entity_list(self, entity_list):
        self.entity_list = entity_list

    def update(self): #미완성
        move_dest = pg.Vector2(0, 0)
        move_dest += self.gravity()
        self.move(move_dest)
        #self.rect.topleft = (int(self.position.x), int(self.position.y))
