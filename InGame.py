import pygame
from map import createMap
from GameOver import gameOver

def startGame():
    #pygame.init() # 초기화

    createMap()  # 맵 및 오브젝트 생성

    from map.setting import players, grounds, bullets, background_image, guns
    from map.init_setting import TICK_PER_SECOND, screen

    # 게임 루프
    running = True
    while running:
        # FPS 설정 (초당 60프레임)
        startTick = pygame.time.get_ticks()

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        grounds.update()  # 바닥 업데이트
        players.update()  # 플레이어 업데이트
        guns.update()  # 총 업데이트
        bullets.update()  # 총알 업데이트
        #print("1총알 개수:", len(bullets))  # 총알 개수 출력 (디버깅용)
        
        for bullet in bullets:
            if not bullet.isExist:
                bullets.remove(bullet)
        #print("2총알 개수:", len(bullets))  # 총알 개수 출력 (디버깅용)
        screen.blit(background_image, (0, 0)) # 배경화면 그리기 (나중에는 이미지 삽입으로 변경)
        grounds.draw(screen) # 플레이어 그리기
        players.draw(screen)  # 플레이어 그리기
        guns.draw(screen)  # 총 그리기
        bullets.draw(screen)  # 총알 그리기

        #print("3총알 개수:", len(bullets))  # 총알 개수 출력 (디버깅용)
        for p in players:
            if p.health <= 0:
                print("플레이어 사망")
                running = False  # 플레이어가 죽으면 게임 종료
                prev_surface = screen.copy()
                overOrder = gameOver(p.type, prev_surface) #나중에 1 바꾸기
                return overOrder

        player_list  = players.sprites()
        # 폰트 설정 (None은 기본 폰트 사용, 40은 글자 크기)c
        font = pygame.font.Font(None, 40)
        # 텍스트 Surface 생성 (텍스트, 안티앨리어싱, 색상)
        text_surface_hp1 = font.render("HP " + str(player_list[0].health), True, (255, 64, 64))
        text_surface_hp2 = font.render("HP " + str(player_list[1].health), True, (64, 64, 255))
        # 텍스트 위치
        text_rect_hp1 = text_surface_hp1.get_rect(topleft=(10, 10))
        text_rect_hp2 = text_surface_hp2.get_rect(topright=(screen.get_width() - 10, 10))
        screen.blit(text_surface_hp1, text_rect_hp1) # 플레이어 1의 HP 표시
        screen.blit(text_surface_hp2, text_rect_hp2) # 플레이어 2의 HP 표시
        
        pygame.display.flip() # 화면 업데이트

        # FPS 조정
        curTick = pygame.time.get_ticks()
        elapsedTime = curTick - startTick
        if elapsedTime < 1000 // TICK_PER_SECOND:
            pygame.time.delay(int(1000 // TICK_PER_SECOND - elapsedTime))