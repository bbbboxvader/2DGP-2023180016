from pico2d import *
import math


open_canvas(800,600)
character = load_image('character.png')

def draw_character(x,y):

    clear_canvas()
    character.draw(x,y)
    update_canvas()
    delay(0.05)

def move_circle():
    for degree in range(360):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)

        draw_character(x,y)
    pass


def move_top():
    print('top')
    for y in range(50, 550, 5):
        draw_character(50, y)
    pass

def move_bottom():
    print('bottom')
    for y in range(550, 50, -5):
        draw_character(750, y)

    pass

def move_right():
    print('right')
    for x in range(50,750,5) :
        draw_character(x,550)
    
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
    #move_circle()
    move_rectangle()
    move_triangle()