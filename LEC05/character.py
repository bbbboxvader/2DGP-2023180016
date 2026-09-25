from pico2d import *
from math import sin, cos

open_canvas(800, 600)
character = load_image('character.png')

angle = 0

while 1:
    for event in get_events():
        if event.type == SDL_QUIT:
            close_canvas()
            raise SystemExit

    x = 400 + 200 * cos(angle)
    y = 300 + 200 * sin(angle)

    clear_canvas()
    character.draw(x, y)
    update_canvas()

    angle += 0.02
    delay(0.01)