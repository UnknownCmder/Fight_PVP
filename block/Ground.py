import pygame as pg

class Ground(pg.sprite.Sprite):
    def __init__(self, image, position: pg.Vector2, size:int):
        super().__init__()
        self.image = image # 이미지 설정
        self.image = pg.transform.scale(self.image, (size, size)) # 이미지 크기 조정
        self.position = position # 위치 설정
        self.rect = self.image.get_rect()  # 히트박스(직사각형)
        self.rect.topleft = (self.position.x, self.position.y) # 직사각형 위치 설정

        self.isExist = True  # 오브젝트 존재 여부

    def update(self):
        pass