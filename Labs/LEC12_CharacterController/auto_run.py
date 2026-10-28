from time import monotonic

from pico2d import get_canvas_width


class AutoRun:
    DURATION = 5.0
    SPEED_MULTIPLIER = 2.0
    SIZE = 150

    def __init__(self, boy):
        self.boy = boy
        self.started_at = None

    def _bounds(self):
        half_size = self.SIZE / 2
        return half_size, get_canvas_width() - half_size

    def enter(self):
        self.started_at = monotonic()
        self.boy.last_update_at = self.started_at
        self.boy.frame = 0
        self.boy.pressed_directions.clear()
        left, right = self._bounds()
        self.boy.x = max(left, min(right, self.boy.x))

    def exit(self):
        self.started_at = None
        self.boy.frame = 0

    def time_out(self):
        return (self.started_at is not None
                and monotonic() - self.started_at >= self.DURATION)

    def update(self):
        self.boy._animate()
        left, right = self._bounds()
        span = right - left
        if span <= 0:
            self.boy.x = get_canvas_width() / 2
            return

        # Fold the travelled distance between the two screen edges. This also
        # preserves overshoot if a slow frame crosses more than one edge.
        offset = self.boy.x - left
        phase = offset if self.boy.face_dir == 1 else 2 * span - offset
        distance = self.boy.RUN_SPEED * self.SPEED_MULTIPLIER * self.boy.frame_time
        phase = (phase + distance) % (2 * span)
        if phase < span:
            self.boy.x = left + phase
            self.boy.face_dir = 1
        else:
            self.boy.x = right - (phase - span)
            self.boy.face_dir = -1

    def draw(self):
        row = 100 if self.boy.face_dir == 1 else 0
        # Raise the center as the sprite grows, keeping its bottom on the grass.
        center_y = self.boy.y + (self.SIZE - 100) / 2
        self.boy.image.clip_draw(
            int(self.boy.frame) * 100, row, 100, 100,
            self.boy.x, center_y, self.SIZE, self.SIZE,
        )
