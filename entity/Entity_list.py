import pygame
import entity.Character as Character
from map import screen_height

RED = (255, 0, 0)
BLUE = (0, 0, 225)


players = pygame.sprite.Group()
player1 = Character.Character("player1", pygame.Vector2(300, screen_height - 50), RED, 50, [pygame.K_a, pygame.K_d, pygame.K_w])
player2 = Character.Character("player2", pygame.Vector2(100, screen_height - 50), BLUE,50, [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP])
players.add(player1)
players.add(player2)

entity_list = (player1, player2) # 엔티티 리스트 (추후 확장 가능성 고려)

for entity in entity_list:
    print("done")
    entity.set_entity_list(entity_list)  # 각 엔티티에 엔티티 리스트 설정