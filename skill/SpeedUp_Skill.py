from .Skill import Skill
from map.CreateMap import players
from Tool import secondToTick
from entity import Character
import pygame as pg
from particle import ExplosionParticle

class SpeedUp_Skill(Skill):
    def __init__(self):
        super().__init__()
        # 쿨타임
        self.init_cooltime = secondToTick(7)
        self.cooltime = 0

        self.user = None

        # 스킬 발동동
        self.speed_increase_amount = 10        
        self.init_duration_time = secondToTick(7)           
        self.duration_time = 0

        self.user_original_speed = 0

        self.use_sound = pg.mixer.Sound("./assets/sounds/speedup_skill.wav")  # 스피드 업 스킬 소리 로드

    def use(self, user: Character):
        if self.cooltime > 0:
            return  # 쿨타임이 남아있으면 스킬 사용 불가
        self.cooltime = self.init_cooltime  # 쿨타임 초기화
        self.duration_time = self.init_duration_time
        self.user = user

        self.use_sound.play()  # 스피드 업 스킬 소리 재생
        self.user_original_speed = user.speed
        user.setSpeed(user.speed + self.speed_increase_amount)

    def update(self):
        if self.user and self.duration_time > 0:
            self.duration_time -= 1
            particle = ExplosionParticle(self.user.position.x + self.user.size.x //2, self.user.position.y + self.user.size.y - 1, max_radius=7, grow_speed=1, duration=20)
            from map.CreateMap import particles
            particles.append(particle)

            if self.duration_time <= 0:
                self.user.setSpeed(self.user_original_speed)
                self.user = None

        super().update()
