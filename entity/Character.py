import pygame as pg
from entity import Entity

class Character(Entity):
    def __init__(self, position: pg.Vector2, color: tuple ,size: int, move_keys: list):
        #self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.Surface((size, size))
        self.image.fill(color)

        super().__init__(self.image, position, size)
        self.move_keys = move_keys # [left, right, jump]

    def setLocation(self, position: pg.Vector2):
        self.position = position
        self.rect.topleft = (self.position.x, self.position.y)

    def control(self):
        keys = pg.key.get_pressed()
        move_dest = pg.Vector2(0, 0)
        #print("contral start")
        if keys[self.move_keys[0]]:
            move_dest.x = -self.speed
            #self.move(pg.Vector2(-self.speed, 0))
        if keys[self.move_keys[1]]:
            #print("donewfijweofewifjwoifjoweijfewiofjweoifjewoijfwefwefwefwf")
            move_dest.x = self.speed
            #self.move(pg.Vector2(self.speed, 0))
        if keys[self.move_keys[2]]:
            #print("j :", self.rect.bottom, screen_height)
            #if self.isCollide(pg.Vector2(self.position.x, self.position.y + 1)) and not self.isCollide(pg.Vector2(self.position.x, self.position.y - 1)):
            if self.dropping is False:
                #print("jump")
                self.jump_power = self.jump_first_power
        
        return move_dest

    def jump(self):
        if self.jump_power > 0:
            #self.move(pg.Vector2(0, -self.jump_power))
            self.jump_power -= 1
            return pg.Vector2(0, -(self.jump_power + 1))
        return pg.Vector2(0, 0)
    
    def update(self):
        move_dest = pg.Vector2(0, 0)
        #self.rect.clamp_ip(pg.Rect(0, 0, screen_width, screen_height - 10)) # 화면 밖으로 나가지 않도록 제한
        # self.move(self.gravity())
        # self.move(self.control())
        # self.move(self.jump())

        # move_dest += self.gravity()
        
        self.gravity() #옆으로 총돌할때 위로 떠오르는 것 방지하기 위해 따로 계산
        move_dest += self.control()  # 플레이어 조작
        move_dest += self.jump()  # 점프 조작
        self.move(move_dest)
        #self.rect.topleft = (int(self.position.x), int(self.position.y))