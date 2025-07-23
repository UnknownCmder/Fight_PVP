import pygame as pg

class Ground(pg.sprite.Sprite):
    def __init__(self, image, position: pg.Vector2):
        super().__init__()  # Sprite 초기화
        self.image = image
        self.image.fill((0, 255, 0))  # 녹색으로 채우기
        self.position = position
        self.rect = self.image.get_rect()  # 위치와 충돌을 위한 사각형 (필수)
        self.rect.topleft = (self.position.x, self.position.y) 

    def update(self):
        pass