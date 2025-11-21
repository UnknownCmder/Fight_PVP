from .Skill import Skill
import pygame as pg
import time
from entity import Character
from Tool import secondToTick
from particle import HealParticle

class Heal(Skill):
    def __init__(self):
        self.heal_amount = 10
        self.init_cooltime = secondToTick(10)
        self.cooltime = 0

    def use(self, user):
        if self.cooltime == 0:
            # 체력 회복
            user.heal(self.heal_amount)

            offsets = [
                (-15, -15),    # 왼쪽 위
                (15, 15),      # 오른쪽 아래
                (15, -15),     # 오른쪽 위
            ]

            for ox, oy in offsets:
                particle = HealParticle(pg.Vector2(user.position.x + ox, user.position.y + oy))
                # 내부 리스트와 전달된 리스트 둘 다에 추가(호출 구조에 따라 하나만 사용해도 됨)
                from map.CreateMap import particles
                particles.append(particle)

            self.cooltime = self.init_cooltime

