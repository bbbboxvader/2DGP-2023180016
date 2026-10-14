from pico2d import *

open_canvas()
TUK_WIDTH, TUK_HEIGHT = 1280,1024
open_canvas(TUK_WIDTH, TUK_HEIGHT)
tuk_ground = load_image('Tuk_GROUND.png')
grass = load_image('grass.png')
character = load_image('animation_sheet.png')


# fill here

def handle_events():
    # fill here
    global running, dir
    global x,y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            x,y = event.x,TUK_HEIGHT -1 -event.y
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running =False
        elif event.type == SDL_KEYDOWN:
            if event.key ==SDLK_RIGHT:
                dir+=1
            elif event.key == SDLK_LEFT:
                dir-=1
            elif event.key ==SDLK_ESCAPE:
                running  = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir-=1
            elif event.key == SDLK_LEFT:
                dir+=1

running = True
x= 800//2
frame = 0
x,y = TUK_WIDTH//2, TUK_HEIGHT//2
hide_cursor()
dir = 0
while running:

    clear_canvas()
    tuk_ground.draw(TUK_WIDTH//2, TUK_HEIGHT//2)
    grass.draw(400, 30)
    character.clip_draw(frame * 100, 100*1, 100, 100, x, y)
    update_canvas()
    handle_events()
    # fill here
    frame = (frame + 1) % 8
    x+=dir*5
    delay(0.05)



close_canvas()
