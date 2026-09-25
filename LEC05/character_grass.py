from pico2d import *

open_canvas()
grass = load_image('grass.png')
character = load_image('character.png')
x = 10
y=40
while game_is_running:
    update_game_logic()
    render_game_state()
    clear_canvas()
    while x<= 700:
        get_events()
        grass.draw(400, 30)
        character.draw(x, y)
        update_canvas()
        x += 2
        clear_canvas()
        delay(0.01)
    while y<=500:
        get_events()
        grass.draw(400, 30)
        character.draw(x, y)
        update_canvas()
        y += 2
        clear_canvas()
        delay(0.01)
    while x>= 10:
        get_events()
        grass.draw(400, 30)
        character.draw(x, y)
        update_canvas()
        x -= 2
        clear_canvas()
        delay(0.01)
    while y>=40:
        get_events()
        grass.draw(400, 30)
        character.draw(x, y)
        update_canvas()
        y -= 2
        clear_canvas()
        delay(0.01)


update_canvas()
delay(5)
close_canvas()