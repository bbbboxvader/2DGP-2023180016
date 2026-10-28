class AutoRun:
    SPEED_MULTIPLIER = 1.0
    SIZE = 100

    def __init__(self, boy):
        self.boy = boy

    def enter(self):
        self.boy.frame = 0

    def exit(self):
        self.boy.frame = 0

    def update(self):
        self.boy._update_run()

    def draw(self):
        row = 100 if self.boy.face_dir == 1 else 0
        self.boy.image.clip_draw(
            int(self.boy.frame) * 100, row, 100, 100,
            self.boy.x, self.boy.y,
        )
