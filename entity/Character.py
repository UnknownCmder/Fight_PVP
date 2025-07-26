import pygame as pg
from entity import Entity

class Character(Entity):
    def __init__(self, image, position: pg.Vector2, size: int, move_keys: list):
        super().__init__(image, position, size)
        self.move_keys = move_keys # [left, right, jump]

    def setLocation(self, position: pg.Vector2): # 위치 설정
        self.position = position
        self.rect.topleft = (self.position.x, self.position.y)

    def control(self): # 플레이어 조작
        keys = pg.key.get_pressed() # 현재 키 상태 가져오기
        move_dest = pg.Vector2(0, 0) # 이동할 거리 초기화

        if keys[self.move_keys[0]]: # 왼쪽 방향키
            move_dest.x = -self.speed
        if keys[self.move_keys[1]]: # 오른쪽 방향키
            move_dest.x = self.speed
        if keys[self.move_keys[2]]: # 점프
            if self.dropping is False:
                self.jump_power = self.jump_first_power
        
        return move_dest

    def jump(self): # 점프
        if self.jump_power > 0:
            self.jump_power -= 1
            return pg.Vector2(0, -(self.jump_power + 1))
        return pg.Vector2(0, 0)
    
    def update(self):
        # 이동
        move_dest = pg.Vector2(0, 0)
        self.gravity()
        move_dest += self.control()  # 플레이어 조작
        move_dest += self.jump()  # 점프 조작
        self.move(move_dest)