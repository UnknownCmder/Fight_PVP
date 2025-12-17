import pygame
import random

# ------------------------------
# 작은 구름(연기) 입자 클래스
# ------------------------------
class CloudParticle:
    def __init__(
        self,
        x,
        y,
        max_radius=20,     # 구름 최대 크기
        grow_speed=0.5,    # 퍼지는 속도
        rise_speed=0.3,    # 위로 올라가는 속도
        duration=60,       # 지속 프레임
        color=(200, 200, 200)
    ):
        self.x = x + random.uniform(-5, 5)
        self.y = y + random.uniform(-5, 5)

        self.radius = random.uniform(6, 10)
        self.max_radius = max_radius
        self.grow_speed = grow_speed
        self.vy = -rise_speed

        self.life = duration
        self.max_life = duration
        self.color = color

    def update(self):
        self.radius = min(self.max_radius, self.radius + self.grow_speed)
        self.y += self.vy
        self.life -= 1

    def draw(self, surface):
        if self.life <= 0:
            return

        alpha = int(180 * (self.life / self.max_life))
        cloud_surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)

        pygame.draw.circle(
            cloud_surf,
            (*self.color, alpha),
            (int(self.x), int(self.y)),
            int(self.radius)
        )
        surface.blit(cloud_surf, (0, 0))

    def is_dead(self):
        return self.life <= 0


# ------------------------------
# 테스트용 메인
# ------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Cloud Particle Test")
    clock = pygame.time.Clock()

    clouds = []

    running = True
    while running:
        clock.tick(60)
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 클릭 시 작은 구름 1개 생성
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                clouds.append(
                    CloudParticle(
                        x, y,
                        max_radius=22,
                        grow_speed=0.4,
                        rise_speed=0.3
                    )
                )

        for cloud in clouds[:]:
            cloud.update()
            cloud.draw(screen)
            if cloud.is_dead():
                clouds.remove(cloud)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
