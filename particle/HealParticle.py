import pygame as pg
import time
from Particle import Particle

class HealParticle(Particle):
    def __init__(self, pos):
        self.position = pos
        self.start_time = time.time()
        self.duration = 2.0  # 2초 후 사라짐
        self.size = 10
        self.alpha = 255

        # 십자 모양 Surface 생성
        self.surface = pg.Surface((20, 20), pg.SRCALPHA)

    def update(self):
        elapsed = time.time() - self.start_time

        if elapsed > self.duration:
            return False  # 효과 종료

        # 점점 사라지는 알파 값 (2초 동안 255 → 0)
        self.alpha = max(0, 255 - int(255 * (elapsed / self.duration)))

        return True

    def draw(self):
        from map.init_setting import screen
        self.surface.fill((0, 0, 0, 0))  # 이전 프레임 지우기

        # 십자 그리기 (두 직선을 겹쳐 십자 모양)
        pg.draw.line(self.surface, (0, 140, 40, self.alpha),
                     (10, 0), (10, 15), 3)
        pg.draw.line(self.surface, (0, 255, 0, self.alpha),
                     (0, 10), (15, 10), 3)

        screen.blit(self.surface, (self.position.x - 10, self.position.y - 10))