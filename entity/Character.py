import pygame as pg
from entity import Entity
from item import Gun

class Character(Entity):
    def __init__(self, type:int, image, position: pg.Vector2, size: int, move_keys: list):
        super().__init__(image, position, size)
        self.type = type # 캐릭터 타입 (1: 플레이어1, 2: 플레이어2)
        self.move_keys = move_keys # [left, right, jump]
        self.health = 1 # 체력
        self.gun = None
        self.didAttack = False  # 공격 여부

    def getGun(self, image, size: int, bullet_speed: int):
        self.gun = Gun(image, pg.Vector2((self.rect.left + self.rect.right) / 2, (self.rect.top + self.rect.bottom) / 2), size, bullet_speed) # 총 생성

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
        if keys[self.move_keys[3]]: # 공격
            if self.gun and not self.didAttack:
                self.gun.shoot(self)
                self.didAttack = True
        else:
            self.didAttack = False
        
        return move_dest
    
    def isCollide(self, move: pg.Vector2): # 충돌 여부 확인
        # 충돌 여부를 확인하기 위해 임시로 rect를 복사
        temp_rect = self.rect.copy()
        temp_rect.x += int(move.x)
        temp_rect.y += int(move.y)

        from map.init_setting import screen_width, screen_height, screen
        from map.setting import players, grounds, bullets
        #if temp_rect.left < 0 or temp_rect.right > screen_width or temp_rect.top < 0 or temp_rect.bottom > screen_height: # 화면 밖으로 나가는지 확인
        #    return True
        old_rect = temp_rect.copy()
        temp_rect.clamp_ip(screen.get_rect())

        if temp_rect.topleft != old_rect.topleft:
            return True

        
        for p in players: # 플레이어와 충돌 체크
            if p != self and temp_rect.colliderect(p.rect):
                return True
        for g in grounds:
            if temp_rect.colliderect(g.rect):
                return True
            
        return False

    def jump(self): # 점프
        if self.jump_power > 0:
            self.jump_power -= 1
            return pg.Vector2(0, -(self.jump_power + 1))
        return pg.Vector2(0, 0)
    
    def damage(self, damage: int): # 피해 받기
        self.health -= damage
        if self.health <= 0:
            self.kill()  # 캐릭터 제거
    
    def update(self):
        # 이동
        move_dest = pg.Vector2(0, 0)
        self.gravity()
        move_dest += self.control()  # 플레이어 조작
        move_dest += self.jump()  # 점프 조작
        self.move(move_dest)

        # 총 위치 업데이트
        self.gun.setLocation(pg.Vector2((self.rect.left + self.rect.right) / 2, (self.rect.top + self.rect.bottom) / 2))
        self.gun.turn(5)  # 총 회전