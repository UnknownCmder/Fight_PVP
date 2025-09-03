import pygame as pg
import sys

# 색상
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

def draw_text_with_border(surface, text, font, text_color, border_color, center_pos, border_thickness=2):
    # 테두리 있는 텍스트 그리기
    text_surface = font.render(text, True, text_color)
    border_surface = font.render(text, True, border_color)
    rect = text_surface.get_rect(center=center_pos)

    # 테두리 여러 방향에 그리기
    for dx in range(-border_thickness, border_thickness+1):
        for dy in range(-border_thickness, border_thickness+1):
            if dx != 0 or dy != 0:
                surface.blit(border_surface, rect.move(dx, dy))

    # 본문 텍스트 덮어쓰기
    surface.blit(text_surface, rect)
    return rect

def gameOver(loser: int, pre_screen):  # 게임 오버 화면
    from map.init_setting import screen, screen_width, screen_height

    # 폰트 설정
    font_big = pg.font.SysFont(None, 100)
    font_small = pg.font.SysFont(None, 60)

    # 메뉴 항목
    menu_items = [
        {"text": "replay", "color": GREEN, "rect": None},
        {"text": "go to lobby", "color": RED, "rect": None}
    ]
    selected_index = 0

    while True:
        screen.blit(pre_screen, (0, 0))  # 이전 화면 그리기

        # 반투명 검은 박스 만들기
        overlay = pg.Surface((screen_width, screen_height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        winner = 0
        if loser == 1:
            winner = 2
        else:
            winner = 1
        # 승자 표시
        rect_gameover = draw_text_with_border(
            screen, f"player{winner} win!", font_big, WHITE, BLACK,
            (screen_width // 2, screen_height // 2 - 100), border_thickness=3
        )

        # 메뉴 표시
        start_y = screen_height // 2
        gap = 80
        for i, item in enumerate(menu_items):
            rect = draw_text_with_border(
                screen, item["text"], font_small, item["color"], BLACK,
                (screen_width // 2, start_y + i * gap), border_thickness=2
            )
            item["rect"] = rect

            # 선택된 메뉴 옆에 삼각형 표시
            if i == selected_index:
                triangle_points = [
                    (rect.left - 30, rect.centery - 10),
                    (rect.left - 30, rect.centery + 10),
                    (rect.left - 10, rect.centery)
                ]
                pg.draw.polygon(screen, WHITE, triangle_points)

        pg.display.flip()

        # 이벤트 처리
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    selected_index = (selected_index + 1) % len(menu_items)
                elif event.key == pg.K_UP or event.key == pg.K_w:
                    selected_index = (selected_index - 1) % len(menu_items)
                elif event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                    return menu_items[selected_index]["text"]
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for i, item in enumerate(menu_items):
                    if item["rect"] and item["rect"].collidepoint(event.pos):
                        return item["text"]
