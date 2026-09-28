from pico2d import *

import math

character = load_image('character.png')

def move_circle():
    for degree in range(360):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)

        clear_canvas()
        character.draw(x, y)
        update_canvas()
        delay(0.05)
    pass

def move_top():
    print('top')
    pass
def move_bottom():
    print('bottom')
    pass
def move_right():
    print('right')
    pass
def move_left():
    print('left')
    pass

def move_rectangle():
    move_top()
    move_right()
    move_left()
    move_bottom()
    pass

def move_triangle():
    pass

while True:
    move_circle()
    move_rectangle()
    move_triangle()