from dataclasses import dataclass
from pathlib import Path


SHEET_WIDTH = 399
SHEET_HEIGHT = 525
SPRITE_SHEET_PATH = Path(__file__).with_name('sonic-sprite.png')


@dataclass(frozen=True)
class Frame:
    left: int
    top: int
    width: int
    height: int


@dataclass(frozen=True)
class Animation:
    name: str
    frames: tuple[Frame, ...]
    frame_interval: float


ANIMATIONS = (
    Animation('Sequence 01', (
        Frame(1, 39, 29, 39),
        Frame(31, 40, 26, 38),
        Frame(58, 39, 28, 39),
        Frame(86, 40, 30, 38),
        Frame(118, 40, 30, 38),
        Frame(150, 40, 30, 38),
        Frame(182, 40, 29, 38),
        Frame(211, 39, 29, 38),
        Frame(240, 39, 29, 38),
        Frame(270, 45, 24, 32),
        Frame(302, 51, 29, 26),
    ), 0.08),
)


def pico_frame_rect(frame: Frame) -> tuple[int, int, int, int]:
    """Convert a top-origin PNG rectangle to Pico2D's bottom-origin coordinates."""
    bottom = SHEET_HEIGHT - frame.top - frame.height
    return frame.left, bottom, frame.width, frame.height


def validate_frame_bounds() -> None:
    for animation in ANIMATIONS:
        if not animation.frames:
            raise ValueError(f'{animation.name} has no frames')
        for frame in animation.frames:
            if frame.left < 0 or frame.top < 0:
                raise ValueError(f'{animation.name} has a negative frame origin')
            if frame.left + frame.width > SHEET_WIDTH:
                raise ValueError(f'{animation.name} exceeds the sprite sheet width')
            if frame.top + frame.height > SHEET_HEIGHT:
                raise ValueError(f'{animation.name} exceeds the sprite sheet height')