import pygame
import sys
from map import createMap
from GameOver import gameOver
from Select_feature import select_feature
from Select_feature import player1_gun, player2_gun, player1_skill, player2_skill
from Tool import draw_text_with_outline

def startGame():
    select_feature()  # 아이템 및 스킬 선택
    createMap()  # 맵 및 오브젝트 생성

    from map.CreateMap import players, grounds, bullets, background_image, guns, mines, particles
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
                pygame.quit()
                sys.exit()

        grounds.update()  # 바닥 업데이트
        players.update()  # 플레이어 업데이트
        guns.update()  # 총 업데이트
        bullets.update()  # 총알 업데이트
        mines.update()  # 지뢰 업데이트
        
        # 없어진 앤티티 구룹에서 제거
        for bullet in bullets:
            if not bullet.isExist:
                bullets.remove(bullet)
        for mine in mines:
            if not mine.isExist:
                mines.remove(mine)

        screen.blit(background_image, (0, 0)) # 배경화면 그리기 (나중에는 이미지 삽입으로 변경)
        grounds.draw(screen) # 플레이어 그리기
        players.draw(screen)  # 플레이어 그리기
        guns.draw(screen)  # 총 그리기
        bullets.draw(screen)  # 총알 그리기
        mines.draw(screen)  # 지뢰 그리기
        for effect in particles: # 파티클 그리기
            if not effect.update():
                particles.remove(effect)
            else:
                effect.draw()

        for p in players:
            if p.health <= 0:
                print("플레이어 사망")
                running = False  # 플레이어가 죽으면 게임 종료
                prev_surface = screen.copy()
                overOrder = gameOver(p.type, prev_surface) #나중에 1 바꾸기
                return overOrder


        player_list  = players.sprites()
        # HP 바 표시 (녹색 채움, HP 감소 시 채움이 줄어들고 빈 공간은 회색)
        bar_width = 320  # 너비 증가
        bar_height = 28  # 높이 증가
        padding = 15
        bar_y = 10
        # 플레이어1 (왼쪽)
        max_hp1 = player_list[0].maximum_health
        cur_hp1 = max(0, player_list[0].health)
        filled_w1 = int(bar_width * (cur_hp1 / max_hp1)) if max_hp1 > 0 else 0
        bg_rect1 = pygame.Rect(padding, bar_y, bar_width, bar_height)
        fill_rect1 = pygame.Rect(padding, bar_y, filled_w1, bar_height)
        pygame.draw.rect(screen, (128, 128, 128), bg_rect1)  # 회색 배경 (빈 공간)
        pygame.draw.rect(screen, (50, 205, 50), fill_rect1)  # 녹색 채움 (현재 HP)
        pygame.draw.rect(screen, (0,0,0), bg_rect1, 2)  # 테두리
        # 플레이어2 (오른쪽)
        max_hp2 = player_list[1].maximum_health
        cur_hp2 = max(0, player_list[1].health)
        filled_w2 = int(bar_width * (cur_hp2 / max_hp2)) if max_hp2 > 0 else 0
        bg_rect2 = pygame.Rect(screen.get_width() - padding - bar_width, bar_y, bar_width, bar_height)
        fill_rect2 = pygame.Rect(screen.get_width() - padding - filled_w2, bar_y, filled_w2, bar_height)  # 오른쪽 정렬
        pygame.draw.rect(screen, (128, 128, 128), bg_rect2)
        pygame.draw.rect(screen, (50, 205, 50), fill_rect2)
        pygame.draw.rect(screen, (0,0,0), bg_rect2, 2)
        

        #스킬 쿨타임 보여주기
        player_list  = players.sprites()
        # 폰트 설정 (None은 기본 폰트 사용, 40은 글자 크기)
        font = pygame.font.Font(None, 40)
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        # 틱을 초로 변환하여 00.0s 포맷으로 표시
        cooltime_sec1 = player_list[0].skill.cooltime / TICK_PER_SECOND
        cooltime_str1 = f"{cooltime_sec1:04.1f}s"
        draw_text_with_outline("CoolTime : " + cooltime_str1, font, WHITE, BLACK, (130, 60), screen, 2) # 플레이어 1의 CoolTime 표시
        cooltime_sec2 = player_list[1].skill.cooltime / TICK_PER_SECOND
        cooltime_str2 = f"{cooltime_sec2:04.1f}s"
        draw_text_with_outline("CoolTime : " + cooltime_str2, font, WHITE, BLACK, (screen.get_width() - 130, 60), screen, 2) # 플레이어 2의 CoolTime 표시


        pygame.display.flip() # 화면 업데이트

        # FPS 조정
        curTick = pygame.time.get_ticks()
        elapsedTime = curTick - startTick
        if elapsedTime < 1000 // TICK_PER_SECOND:
            pygame.time.delay(int(1000 // TICK_PER_SECOND - elapsedTime))