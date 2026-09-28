# 실습 과제 진행

from pico2d import *

open_canvas(800,600)

character = load_image('character.png')


def move_circle() :
    circle_x=400
    circle_y=300
    clear_canvas()
    character.draw(circle_x, circle_y)
    update_canvas()
    print("circle")
    pass

def move_rectangle():
    print("rectangle")
    pass

def move_triangle():
    print("triangle")
    pass

while True :
    move_circle()
    move_rectangle()
    move_triangle()
    pass