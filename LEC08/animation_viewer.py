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


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    sprite_sheet = load_image('SamuraiSheet.png')
    clear_canvas()
    sprite_sheet.clip_draw(0, 1152, 128, 128, 320, 240)
    update_canvas()
    delay(2)
    close_canvas()


if __name__ == '__main__':
    main()
