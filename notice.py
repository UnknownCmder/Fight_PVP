import pygame

# 초기화
pygame.init()

# 게임 루프
running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip() # 화면 업데이트

# 종료
pygame.quit()