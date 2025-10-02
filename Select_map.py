import pygame as py
import os

selected_map = "RANDOM"

def draw_text_with_outline(text, font, text_color, outline_color, pos, surface):
    x, y = pos
    # 테두리 그리기
    for dx in [-2, -1, 0, 1, 2]:
        for dy in [-2, -1, 0, 1, 2]:
            if dx != 0 or dy != 0:
                outline_surface = font.render(text, True, outline_color)
                rect = outline_surface.get_rect(center=(x + dx, y + dy))
                surface.blit(outline_surface, rect)
    # 글자 본체 그리기
    text_surface = font.render(text, True, text_color)
    rect = text_surface.get_rect(center=pos)
    surface.blit(text_surface, rect)

def select_map():
    global selected_map
    from map.init_setting import screen, screen_height, screen_width

    # 색상
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    # 폰트
    font_current = py.font.SysFont(None, 50)   # 현재 맵
    font_other = py.font.SysFont(None, 35)     # 이전/다음 맵

    # map_list 폴더의 csv 파일 불러오기
    folder_path = "map/map_list"
    file_list = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    file_list.sort()
    file_list.insert(0, "Random")  # 랜덤 맨 위 추가

    current_index = 0
    running = True
    while running:
        screen.fill((0, 0, 0)) # 배경화면 그리기
        
        # 표시할 맵 이름
        prev_map = file_list[current_index - 1] if current_index > 0 else ""
        next_map = file_list[current_index + 1] if current_index < len(file_list) - 1 else ""
        current_map = file_list[current_index]

        # 이전 맵
        if prev_map:
            draw_text_with_outline(prev_map, font_other, BLACK, WHITE, (screen_width // 2, screen_height // 2 - 40), screen)
        
        # 현재 맵
        draw_text_with_outline(current_map, font_current, RED, WHITE, (screen_width // 2, screen_height // 2), screen)
        
        # 다음 맵
        if next_map:
            draw_text_with_outline(next_map, font_other, BLACK, WHITE, (screen_width // 2, screen_height // 2 + 40), screen)

        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            elif event.type == py.KEYDOWN:
                if event.key in [py.K_w, py.K_UP]:
                    if current_index > 0:
                        current_index -= 1
                elif event.key in [py.K_s, py.K_DOWN]:
                    if current_index < len(file_list) - 1:
                        current_index += 1
                elif event.key in [py.K_SPACE, py.K_RETURN]:
                    if current_map == file_list[0]:
                        selected_map = "RANDOM"
                    else:
                        selected_map = current_map
                    running = False

        py.display.flip()
