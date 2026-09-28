from pico2d import *
from math import *

open_canvas(800, 600)

character = load_image('character.png')

running = True
MOVE_STEP = 2.0
FRAME_DELAY = 0.01


def handle_events():
    global running

    for event in get_events():
        if event.type == SDL_QUIT:
            running = False

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False

    return running


def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(FRAME_DELAY)


# 두 점 사이를 직선으로 이동하는 함수
def move_line(start_x, start_y, end_x, end_y):
    distance = hypot(end_x - start_x, end_y - start_y)
    move_count = max(1, int(distance / MOVE_STEP))

    for i in range(move_count + 1):
        if not handle_events():
            return False

        ratio = i / move_count

        x = start_x + (end_x - start_x) * ratio
        y = start_y + (end_y - start_y) * ratio

        draw_character(x, y)

    return True


def move_circle():
    angle = 0

    while angle < 2 * pi:
        if not handle_events():
            return False

        circle_x = 400 + 200 * cos(angle)
        circle_y = 300 + 200 * sin(angle)

        draw_character(circle_x, circle_y)

        angle += 0.02

    print("circle")
    return True


def move_rectangle():
    # 왼쪽 아래 → 오른쪽 아래
    if not move_line(200, 150, 600, 150):
        return False

    # 오른쪽 아래 → 오른쪽 위
    if not move_line(600, 150, 600, 450):
        return False

    # 오른쪽 위 → 왼쪽 위
    if not move_line(600, 450, 200, 450):
        return False

    # 왼쪽 위 → 왼쪽 아래
    if not move_line(200, 450, 200, 150):
        return False

    print("rectangle")
    return True


def move_triangle():
    # 왼쪽 아래 → 오른쪽 아래
    if not move_line(266, 200, 532, 200):
        return False

    # 오른쪽 아래 → 위쪽 꼭짓점
    if not move_line(532, 200, 400, 400):
        return False

    # 위쪽 꼭짓점 → 왼쪽 아래
    if not move_line(400, 400, 266, 200):
        return False

    print("triangle")
    return True


while running:
    if not move_circle():
        break

    if not move_rectangle():
        break

    if not move_triangle():
        break


close_canvas()