from time import monotonic


class AutoRun:
    DURATION = 5.0
    SPEED_MULTIPLIER = 1.0
    SIZE = 100

    def __init__(self, boy):
        self.boy = boy
        self.started_at = None

    def enter(self):
        self.started_at = monotonic()
        self.boy.last_update_at = self.started_at
        self.boy.frame = 0
        self.boy.pressed_directions.clear()

    def exit(self):
        self.started_at = None
        self.boy.frame = 0

    def time_out(self):
        return (self.started_at is not None
                and monotonic() - self.started_at >= self.DURATION)

    def update(self):
        self.boy._update_run()

    def draw(self):
        row = 100 if self.boy.face_dir == 1 else 0
        self.boy.image.clip_draw(
            int(self.boy.frame) * 100, row, 100, 100,
            self.boy.x, self.boy.y,
        )
