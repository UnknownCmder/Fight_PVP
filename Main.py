import pygame
from map import createMap
import sys

# 초기화
pygame.init()

# 색상
WHITE = (255, 255, 255)
createMap()  # 맵 및 오브젝트 생성

from map.setting import screen, TICK_PER_SECOND, player1, player2, players, objects

# 게임 루프
running = True
while running:
    # FPS 설정 (초당 60프레임)
    startTick = pygame.time.get_ticks()

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    players.update()  # 플레이어 업데이트
    objects.update()  # 오브젝트 업데이트

    screen.fill(WHITE) # 배경화면 그리기
    #EntityList.players.update() # 플레이어 업데이트
    objects.draw(screen) # 플레이어 그리기
    pygame.display.flip() # 화면 업데이트

    # FPS 조정
    curTick = pygame.time.get_ticks()
    elapsedTime = curTick - startTick
    if elapsedTime < 1000 // TICK_PER_SECOND:
        pygame.time.delay(int(1000 // TICK_PER_SECOND - elapsedTime))

# 종료
pygame.quit()
sys.exit()