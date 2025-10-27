import pygame as pg
from .Gun import Gun
from entity.Bullet import Bullet

class Pistol(Gun):
    def __init__(self, image, position: pg.Vector2):
        super().__init__(image, position, size=80, bullet_speed=20)

    def shoot(self, shooter):
        image = pg.image.load("./assets/bullet.png").convert_alpha()
        image = pg.transform.rotate(image, -self.angle)
        # 총알 생성
        from map.CreateMap import bullets
        bullets.add(Bullet(image, self.position, 20, pg.Vector2(0, self.bullet_speed).rotate(self.angle), shooter, 2)) # 총알 생성