from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('animation_sheet.png')

count = 0

def running_animation(s,e,r,X):
    frame = 0
    for i in range(s,e,r):
            clear_canvas()
            grass.draw(400,30)
            character.clip_draw(
                100*frame,X,
                100,100,
                i,90,
                100,100
            )
            update_canvas()
            frame = (frame+1)%8
            delay(0.05)
# fill here


while count<4:
    
    running_animation(0)
    running_animation(100)

    count+=1

close_canvas()

