import pygame as pg
from entity.Bullet import Bullet

class Gun(pg.sprite.Sprite):
    def __init__(self, image, position: pg.Vector2, size: int, bullet_speed: int):
        super().__init__()
        self.image = image # 이미지 설정
        self.image = pg.transform.scale(self.image, (size, size)) # 이미지 크기 조정
        self.position = position # 위치 설정
        self.rect = self.image.get_rect()  # 히트박스(직사각형)
        self.rect.center = position  # 직사각형 위치 설정
        self.isExist = True  # 오브젝트 존재 여부
        self.turnedImage = []
        self.bullet_speed = bullet_speed  # 총알 속도 설정

        for i in range(0, 360):
            rotated_image = pg.transform.rotate(self.image, -i)
            self.turnedImage.append(rotated_image)

        self.angle = 0 # 총의 각도

    def turn(self, angle: int):
        self.angle += angle
        self.angle %= 360

        old_center = self.rect.center  # 회전 전 중심 저장
        #self.image = pg.transform.rotate(self.image, self.angle)
        self.image = self.turnedImage[self.angle]
        self.rect = self.image.get_rect(center=old_center)

    def setLocation(self, position: pg.Vector2): # 위치 설정
        self.position = position
        self.rect.center = position

    def shoot(self, shooter):
        image = pg.image.load("./assets/bullet.png").convert_alpha()
        image = pg.transform.rotate(image, -self.angle)
        # 총알 생성
        from map.setting import bullets
        bullets.add(Bullet(image, self.position, 20, pg.Vector2(0, self.bullet_speed).rotate(self.angle), shooter)) # 총알 생성


    def update(self):
        pass