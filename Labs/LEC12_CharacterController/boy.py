from pico2d import load_image
from time import monotonic
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
            states=[{'name': 'IDLE', 'on_enter': '_enter_idle'}],
            initial='IDLE',
            auto_transitions=False,
            transitions=[
                {
                    'trigger': 'tick',
                    'source': 'IDLE',
                    # Internal transition: animate without leaving IDLE.
                    'dest': None,
                    'after': '_animate_idle',
                },
            ],
        )

        self._enter_idle()

    def _enter_idle(self):
        self.frame = 0
        self.idle_started_at = monotonic()

    def _idle_time_expired(self):
        return monotonic() - self.idle_started_at >= self.IDLE_TIMEOUT

    def _animate_idle(self):
        self.frame = (self.frame + 1) % 8

    def update(self):
        self.tick()

    def draw(self):
        if self.face_dir == 1:
            self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)
