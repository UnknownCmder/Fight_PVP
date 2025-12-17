import pygame
# ------------------------------
# 폭발 플래시 (채워진 원)
# ------------------------------
class ExplosionParticle:
    def __init__(
        self,
        x,
        y,
        max_radius=90,
        grow_speed=12,
        duration=18,
        color=(255, 180, 50)
    ):
        self.x = x
        self.y = y
        self.radius = 0
        self.max_radius = max_radius
        self.grow_speed = grow_speed
        self.life = duration
        self.max_life = duration
        self.color = color

    def update(self):
        self.radius += self.grow_speed
        self.life -= 1

        return not self.is_dead()

    def draw(self):
        if self.life <= 0:
            return

        from map.init_setting import screen
        alpha = int(255 * (self.life / self.max_life))
        flash_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        pygame.draw.circle(
            flash_surf,
            (*self.color, alpha),
            (int(self.x), int(self.y)),
            int(self.radius)
        )
        screen.blit(flash_surf, (0, 0))

    def is_dead(self):
        return self.life <= 0 or self.radius >= self.max_radius