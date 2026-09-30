from pico2d import (
    clear_canvas,
    close_canvas,
    delay,
    load_image,
    open_canvas,
    update_canvas,
)


CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480
DRAW_SIZE = 384
FRAME_SIZE = 128
SHEET_HEIGHT = 1280
IDLE_ROW = 0
IDLE_FRAME_COUNT = 6


def frame_rect(row, column):
    left = column * FRAME_SIZE
    bottom = SHEET_HEIGHT - (row + 1) * FRAME_SIZE
    return left, bottom, FRAME_SIZE, FRAME_SIZE


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    sprite_sheet = load_image('SamuraiSheet.png')
    for frame in range(IDLE_FRAME_COUNT):
        clear_canvas()
        left, bottom, width, height = frame_rect(IDLE_ROW, frame)
        sprite_sheet.clip_draw(
            left, bottom, width, height,
            CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2,
            DRAW_SIZE, DRAW_SIZE,
        )
        update_canvas()
        delay(0.1)
    close_canvas()


if __name__ == '__main__':
    main()
