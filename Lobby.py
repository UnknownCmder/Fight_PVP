import pygame as py
import sys
from InGame import startGame
from map import createMap

def start_lobby():
    from map.init_setting import screen_width, screen_height, screen

    # 색상 정의
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    GRAY = (128, 128, 128)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)

    # 글꼴 설정
    title_font = py.font.SysFont(None, 50)
    menu_font = py.font.SysFont(None, 40)

    # 메뉴 항목
    menu_items = [
        {"text": "play", "color": GREEN, "rect": None},
        {"text": "setting", "color": GRAY, "rect": None},
        {"text": "exit", "color": RED, "rect": None}
    ]

    selected_index = 0  # 현재 선택된 메뉴

    # 메인 루프
    running = True
    while running:
        image = py.image.load("./assets/lobby_background.png").convert() # 배경 이미지 불러오기
        screen.blit(image, (-190, 0)) # 배경화면 그리기

        # 메뉴 그리기
        start_y = screen_height//2
        gap = 50
        for i, item in enumerate(menu_items):
            # --- 테두리용 텍스트 (검은색) ---
            border_surface = menu_font.render(item["text"], True, BLACK)
            text_surface = menu_font.render(item["text"], True, item["color"])
            text_rect = text_surface.get_rect(center=(screen_width//2, start_y + i*gap))

            # 테두리(검은색) 먼저 그림 (상하좌우 1픽셀 이동)
            for dx, dy in [(-3,0), (3,0), (0,-3), (0,3)]:
                screen.blit(border_surface, text_rect.move(dx, dy))

            # 본 텍스트(원래 색) 덮어쓰기
            screen.blit(text_surface, text_rect)

            # rect 저장 (클릭 감지용)
            item["rect"] = text_rect

            # 선택된 메뉴 옆에 삼각형 표시
            if i == selected_index:
                triangle_points = [
                    (text_rect.left - 30, text_rect.centery - 10),
                    (text_rect.left - 30, text_rect.centery + 10),
                    (text_rect.left - 10, text_rect.centery)
                ]
                py.draw.polygon(screen, BLACK, triangle_points)


        py.display.flip()

        # 이벤트 처리
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            elif event.type == py.KEYDOWN:
                if event.key == py.K_DOWN or event.key == py.K_s:
                    selected_index = (selected_index + 1) % len(menu_items)
                elif event.key == py.K_UP or event.key == py.K_w:
                    selected_index = (selected_index - 1) % len(menu_items)
                elif event.key == py.K_SPACE:
                    if menu_items[selected_index]["text"] == "play":
                        play()
                    elif menu_items[selected_index]["text"] == "exit":
                        running = False
                    #print(menu_items[selected_index]["text"])
            elif event.type == py.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for item in menu_items:
                    if item["rect"] and item["rect"].collidepoint(mouse_pos):
                        if item["text"] == "play":
                            play()
                        #print(f"{item['text']} clicked!")  # 클릭된 메뉴 출력
                        if item["text"] == "exit":
                            running = False
    py.quit()
    sys.exit()

def play():
    game_running = True
    while game_running:
        result = startGame()  # 게임 시작
        if result == "lobby":
            print("로비로 돌아가기")
            game_running = False  # 종료
        elif result == "replay":
            print("게임 다시 시작")
            continue  # 게임 다시 시작
        else:
            game_running = False  # 종료
            break