from math import pi
from time import monotonic

from pico2d import load_image
from transitions import Machine


class Boy:
    IDLE_TIMEOUT = 5.0

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.image = load_image('animation_sheet.png')
        self.state_machine = Machine(
            model=self,
            states=[
                {'name': 'IDLE', 'on_enter': '_enter_idle'},
                {'name': 'SLEEP', 'on_enter': '_enter_sleep'},
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
                    'after': '_animate_idle',
                },
                {'trigger': 'tick', 'source': 'SLEEP', 'dest': None},
            ],
        )
        # Machine's initial state does not invoke on_enter callbacks.
        self._enter_idle()

    def _enter_idle(self):
        self.frame = 0
        self.idle_started_at = monotonic()

    def _enter_sleep(self):
        self.frame = 0

    def _idle_time_expired(self):
        return monotonic() - self.idle_started_at >= self.IDLE_TIMEOUT

    def _animate_idle(self):
        self.frame = (self.frame + 1) % 8

    def update(self):
        self.tick()

    def draw(self):
        row = 300 if self.face_dir == 1 else 200
        if self.is_SLEEP():
            self.image.clip_composite_draw(
                0, row, 100, 100, -self.face_dir * pi / 2, '',
                self.x, self.y - 25, 100, 100,
            )
        else:
            self.image.clip_draw(self.frame * 100, row, 100, 100, self.x, self.y)
