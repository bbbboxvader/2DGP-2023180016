from typing import NamedTuple

from pico2d import (
    clear_canvas,
    close_canvas,
    delay,
    get_events,
    load_image,
    open_canvas,
    SDL_KEYDOWN,
    SDLK_ESCAPE,
    SDL_QUIT,
    update_canvas,
)


CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480
DRAW_SIZE = 384
FRAME_SIZE = 128
SHEET_HEIGHT = 1280
IDLE_ROW = 0
IDLE_FRAME_COUNT = 6
WALK_ROW = 1
WALK_FRAME_COUNT = 8
RUN_ROW = 2
RUN_FRAME_COUNT = 8
DASH_ROW = 3
DASH_FRAME_COUNT = 12
ACTION_DURATION = 1.0


class Animation(NamedTuple):
    name: str
    row: int
    frame_count: int


ACTIONS = (
    Animation('Idle', IDLE_ROW, IDLE_FRAME_COUNT),
    Animation('Walk', WALK_ROW, WALK_FRAME_COUNT),
    Animation('Run', RUN_ROW, RUN_FRAME_COUNT),
    Animation('Dash', DASH_ROW, DASH_FRAME_COUNT),
)


def frame_rect(row, column):
    left = column * FRAME_SIZE
    bottom = SHEET_HEIGHT - (row + 1) * FRAME_SIZE
    return left, bottom, FRAME_SIZE, FRAME_SIZE


def next_action_index(current):
    return (current + 1) % len(ACTIONS)


def draw_frame(sprite_sheet, action, frame):
    clear_canvas()
    left, bottom, width, height = frame_rect(action.row, frame)
    sprite_sheet.clip_draw(
        left, bottom, width, height,
        CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2,
        DRAW_SIZE, DRAW_SIZE,
    )
    update_canvas()


def should_quit():
    for event in get_events():
        if event.type == SDL_QUIT:
            return True
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return True
    return False


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    sprite_sheet = load_image('SamuraiSheet.png')
    action_index = 0
    running = True
    while running:
        action = ACTIONS[action_index]
        for frame in range(action.frame_count):
            if should_quit():
                running = False
                break
            draw_frame(sprite_sheet, action, frame)
            delay(ACTION_DURATION / action.frame_count)
        if running:
            action_index = next_action_index(action_index)
    close_canvas()


if __name__ == '__main__':
    main()
