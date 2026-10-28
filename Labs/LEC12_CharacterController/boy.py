from math import pi
from time import monotonic

from pico2d import (
    SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_SPACE, SDLK_a,
    get_canvas_width, load_image,
)
from transitions import Machine

from auto_run import AutoRun


class Boy:
    IDLE_TIMEOUT = 5.0
    RUN_SPEED = 200.0  # Pixels per second.
    ANIMATION_FPS = 10.0

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        # The most recently pressed direction takes priority.
        self.pressed_directions = []
        self.frame_time = 0.0
        self.image = load_image('animation_sheet.png')
        self.auto_run = AutoRun(self)
        self.state_machine = Machine(
            model=self,
            states=[
                {'name': 'IDLE', 'on_enter': '_enter_idle'},
                {'name': 'SLEEP', 'on_enter': '_enter_sleep'},
                {'name': 'RUN', 'on_enter': '_enter_run'},
                {'name': 'AUTO_RUN', 'on_enter': self.auto_run.enter,
                 'on_exit': self.auto_run.exit},
            ],
            initial='IDLE',
            auto_transitions=False,
            transitions=[
                {
                    'trigger': 'tick',
                    'source': 'IDLE',
                    'dest': 'SLEEP',
                    'conditions': '_idle_time_expired',
                },
                {
                    'trigger': 'tick',
                    'source': 'IDLE',
                    # Internal transition: animate without leaving IDLE.
                    'dest': None,
                    'after': '_animate',
                },
                {'trigger': 'tick', 'source': 'SLEEP', 'dest': None},
                {'trigger': 'tick', 'source': 'RUN', 'dest': None,
                 'after': '_update_run'},
                {'trigger': 'tick', 'source': 'AUTO_RUN', 'dest': 'IDLE',
                 'conditions': self.auto_run.time_out},
                {'trigger': 'tick', 'source': 'AUTO_RUN', 'dest': None,
                 'after': self.auto_run.update},
                {'trigger': 'wake_up', 'source': 'SLEEP', 'dest': 'IDLE'},
                {'trigger': 'start_running', 'source': ['IDLE', 'SLEEP'],
                 'dest': 'RUN'},
                {'trigger': 'start_running', 'source': 'RUN', 'dest': None},
                {'trigger': 'stop_running', 'source': 'RUN', 'dest': 'IDLE'},
                {'trigger': 'activate_auto_run', 'source': 'IDLE', 'dest': 'AUTO_RUN'},
            ],
        )
        # Machine's initial state does not invoke on_enter callbacks.
        self._enter_idle()

    def _enter_idle(self):
        self.frame = 0
        self.idle_started_at = monotonic()
        self.last_update_at = self.idle_started_at

    def _enter_sleep(self):
        self.frame = 0

    def _enter_run(self):
        self.frame = 0
        self.last_update_at = monotonic()

    def _idle_time_expired(self):
        return monotonic() - self.idle_started_at >= self.IDLE_TIMEOUT

    def _animate(self):
        self.frame = (self.frame + self.ANIMATION_FPS * self.frame_time) % 8

    def _update_run(self):
        self._animate()
        self.x += self.face_dir * self.RUN_SPEED * self.frame_time
        # Keep the entire 100-pixel sprite inside the canvas.
        self.x = max(50, min(get_canvas_width() - 50, self.x))

    def update(self):
        now = monotonic()
        self.frame_time = max(0.0, now - self.last_update_at)
        self.last_update_at = now
        self.tick()

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key in (SDLK_LEFT, SDLK_RIGHT):
            # Ignore OS key-repeat events, preserving the latest direction.
            if event.key in self.pressed_directions:
                return
            self.pressed_directions.append(event.key)
            self.face_dir = -1 if event.key == SDLK_LEFT else 1
            self.start_running()
        elif event.type == SDL_KEYUP and event.key in self.pressed_directions:
            self.pressed_directions.remove(event.key)
            if self.pressed_directions:
                self.face_dir = -1 if self.pressed_directions[-1] == SDLK_LEFT else 1
            elif self.is_RUN():
                self.stop_running()
        elif (event.type == SDL_KEYDOWN and event.key == SDLK_a
                and self.is_IDLE()):
            self.activate_auto_run()
        elif (event.type == SDL_KEYDOWN and event.key == SDLK_SPACE
                and self.is_SLEEP()):
            self.wake_up()

    def draw(self):
        row = 300 if self.face_dir == 1 else 200
        if self.is_AUTO_RUN():
            self.auto_run.draw()
        elif self.is_SLEEP():
            self.image.clip_composite_draw(
                0, row, 100, 100, -self.face_dir * pi / 2, '',
                self.x, self.y - 25, 100, 100,
            )
        elif self.is_RUN():
            row = 100 if self.face_dir == 1 else 0
            self.image.clip_draw(int(self.frame) * 100, row, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(int(self.frame) * 100, row, 100, 100, self.x, self.y)
