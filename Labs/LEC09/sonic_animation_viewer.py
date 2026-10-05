from dataclasses import dataclass
from math import isfinite, pi, sin
from pathlib import Path
from typing import Any

from pico2d import (
    clear_canvas,
    close_canvas,
    delay,
    get_events,
    get_time,
    load_image,
    open_canvas,
    SDL_KEYDOWN,
    SDLK_ESCAPE,
    SDL_QUIT,
    update_canvas,
)


SHEET_WIDTH = 399
SHEET_HEIGHT = 525
SPRITE_SHEET_PATH = Path(__file__).with_name('sonic-sprite.png')
CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480
CANVAS_MARGIN = 24
MAX_DISPLAY_SCALE = 4.0
POLL_DELAY = 0.001


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
    movement_direction: tuple[int, int] = (0, 0)
    jump_arc: int = 0


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
    ), 0.08, movement_direction=(1, 0)),
)

ANIMATIONS += (
    Animation('Sequence 02', (
        Frame(8, 80, 26, 37),
        Frame(37, 80, 27, 37),
        Frame(65, 80, 31, 38),
        Frame(97, 80, 37, 37),
        Frame(135, 80, 32, 35),
        Frame(170, 79, 32, 38),
        Frame(206, 79, 26, 38),
        Frame(238, 80, 24, 37),
        Frame(263, 80, 30, 37),
        Frame(295, 80, 36, 37),
        Frame(334, 80, 32, 36),
        Frame(370, 79, 29, 38),
    ), 0.075, movement_direction=(1, 0)),
)

ANIMATIONS += (
    Animation('Sequence 03', (
        Frame(1, 124, 33, 40),
        Frame(39, 124, 35, 39),
        Frame(89, 125, 35, 38),
        Frame(130, 121, 34, 42),
        Frame(181, 122, 34, 41),
        Frame(228, 122, 33, 40),
    ), 0.09, movement_direction=(1, 0), jump_arc=90),
)

ANIMATIONS += (
    Animation('Sequence 04', (
        Frame(1, 169, 29, 30),
        Frame(35, 167, 29, 31),
        Frame(67, 169, 30, 29),
        Frame(98, 169, 31, 29),
        Frame(131, 168, 29, 30),
        Frame(162, 168, 29, 31),
        Frame(193, 170, 30, 29),
        Frame(230, 170, 31, 29),
    ), 0.07),
)

ANIMATIONS += (
    Animation('Sequence 05', (
        Frame(1, 206, 30, 27),
        Frame(36, 206, 29, 27),
        Frame(70, 206, 29, 27),
        Frame(105, 206, 29, 27),
        Frame(139, 206, 29, 27),
        Frame(174, 206, 29, 27),
        Frame(1, 239, 29, 35),
        Frame(36, 239, 30, 35),
        Frame(74, 239, 31, 35),
        Frame(111, 238, 31, 36),
        Frame(149, 239, 30, 35),
        Frame(186, 238, 31, 36),
    ), 0.065, movement_direction=(1, 0)),
)

ANIMATIONS += (
    Animation('Sequence 06', (
        Frame(1, 283, 29, 35),
        Frame(36, 283, 30, 35),
        Frame(72, 286, 39, 31),
        Frame(123, 285, 39, 32),
        Frame(172, 286, 39, 31),
        Frame(218, 285, 38, 32),
    ), 0.085),
)

ANIMATIONS += (
    Animation('Sequence 07', (
        Frame(1, 326, 24, 45),
        Frame(31, 327, 29, 44),
        Frame(65, 327, 20, 44),
        Frame(90, 327, 25, 43),
        Frame(119, 327, 25, 43),
        Frame(149, 327, 20, 44),
        Frame(184, 341, 40, 28),
        Frame(232, 341, 39, 27),
    ), 0.08),
)

ANIMATIONS += (
    Animation('Sequence 08', (
        Frame(1, 379, 27, 38),
        Frame(31, 379, 31, 36),
        Frame(64, 379, 31, 36),
        Frame(99, 377, 33, 38),
        Frame(136, 379, 32, 36),
        Frame(176, 379, 33, 36),
        Frame(217, 379, 33, 36),
        Frame(254, 378, 33, 36),
    ), 0.075, movement_direction=(1, 0)),
)

ANIMATIONS += (
    Animation('Sequence 09', (
        Frame(6, 429, 34, 40),
        Frame(49, 426, 34, 43),
        Frame(96, 427, 23, 39),
        Frame(125, 427, 23, 39),
    ), 0.11),
)

REPEATS_PER_ANIMATION = 5
INTER_ANIMATION_DELAY = 1.0


@dataclass
class PlaybackState:
    animation_index: int = 0
    frame_index: int = 0
    completed_cycles: int = 0
    wait_until: float | None = None
    next_frame_at: float = 0.0


def advance_frame(state: PlaybackState) -> bool:
    animation = ANIMATIONS[state.animation_index]
    state.frame_index += 1
    if state.frame_index < len(animation.frames):
        return False
    state.frame_index = 0
    return True


def record_completed_cycle(state: PlaybackState, completed_at: float) -> bool:
    state.completed_cycles += 1
    if state.completed_cycles < REPEATS_PER_ANIMATION:
        return False
    state.frame_index = len(ANIMATIONS[state.animation_index].frames) - 1
    state.wait_until = completed_at + INTER_ANIMATION_DELAY
    return True


def finish_inter_animation_wait(state: PlaybackState, now: float) -> bool:
    if state.wait_until is None or now < state.wait_until:
        return False
    state.animation_index = next_animation_index(state.animation_index)
    state.frame_index = 0
    state.completed_cycles = 0
    state.wait_until = None
    state.next_frame_at = now + ANIMATIONS[state.animation_index].frame_interval
    return True


def tick_inter_animation_wait(state: PlaybackState, now: float) -> bool:
    if state.wait_until is None:
        return False
    finish_inter_animation_wait(state, now)
    return True


def advance_timeline(state: PlaybackState, now: float) -> bool:
    if state.wait_until is not None:
        return finish_inter_animation_wait(state, now)
    if now < state.next_frame_at:
        return False

    changed = False
    while now >= state.next_frame_at and state.wait_until is None:
        animation = ANIMATIONS[state.animation_index]
        completed_at = state.next_frame_at
        cycle_completed = advance_frame(state)
        state.next_frame_at += animation.frame_interval
        changed = True
        if cycle_completed and record_completed_cycle(state, completed_at):
            break
    return changed


def animation_progress(state: PlaybackState) -> float:
    frame_count = len(ANIMATIONS[state.animation_index].frames)
    progress = (state.completed_cycles + state.frame_index / frame_count) / REPEATS_PER_ANIMATION
    return min(1.0, max(0.0, progress))


def scaled_frame_size(frame: Frame, vertical_arc: int = 0) -> tuple[int, int]:
    available_width = CANVAS_WIDTH - 2 * CANVAS_MARGIN
    available_height = CANVAS_HEIGHT - 2 * CANVAS_MARGIN - 2 * vertical_arc
    if available_height <= 0:
        raise ValueError('vertical movement leaves no room to draw the frame')
    scale = min(
        MAX_DISPLAY_SCALE,
        available_width / frame.width,
        available_height / frame.height,
    )
    return max(1, round(frame.width * scale)), max(1, round(frame.height * scale))


def frame_position(
    animation: Animation,
    draw_width: int,
    draw_height: int,
    progress: float,
) -> tuple[int, int]:
    progress = min(1.0, max(0.0, progress))
    center_x = CANVAS_WIDTH // 2
    center_y = CANVAS_HEIGHT // 2
    direction_x, direction_y = animation.movement_direction

    if direction_x:
        left = CANVAS_MARGIN + draw_width // 2
        right = CANVAS_WIDTH - CANVAS_MARGIN - (draw_width - draw_width // 2)
        center_x = round(left + (right - left) * (progress if direction_x > 0 else 1 - progress))
    if direction_y:
        bottom = CANVAS_MARGIN + draw_height // 2
        top = CANVAS_HEIGHT - CANVAS_MARGIN - (draw_height - draw_height // 2)
        center_y = round(bottom + (top - bottom) * (progress if direction_y > 0 else 1 - progress))
    if animation.jump_arc:
        center_y += round(sin(pi * progress) * animation.jump_arc)
    return center_x, center_y


def draw_frame(
    sprite_sheet: Any,
    animation: Animation,
    frame_index: int,
    progress: float = 0.5,
) -> None:
    frame = animation.frames[frame_index]
    draw_width, draw_height = scaled_frame_size(frame, animation.jump_arc)
    center_x, center_y = frame_position(animation, draw_width, draw_height, progress)
    clear_canvas()
    sprite_sheet.clip_draw(
        *pico_frame_rect(frame),
        center_x,
        center_y,
        draw_width,
        draw_height,
    )
    update_canvas()


def should_quit() -> bool:
    for event in get_events():
        if event.type == SDL_QUIT:
            return True
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return True
    return False


def main() -> None:
    validate_frame_bounds()
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        sprite_sheet = load_image(str(SPRITE_SHEET_PATH))
        state = PlaybackState(
            next_frame_at=get_time() + ANIMATIONS[0].frame_interval,
        )
        while not should_quit():
            advance_timeline(state, get_time())
            animation = ANIMATIONS[state.animation_index]
            draw_frame(
                sprite_sheet,
                animation,
                state.frame_index,
                animation_progress(state),
            )
            delay(POLL_DELAY)
    finally:
        close_canvas()


def pico_frame_rect(frame: Frame) -> tuple[int, int, int, int]:
    """Convert a top-origin PNG rectangle to Pico2D's bottom-origin coordinates."""
    bottom = SHEET_HEIGHT - frame.top - frame.height
    return frame.left, bottom, frame.width, frame.height


def validate_frame_bounds() -> None:
    for animation in ANIMATIONS:
        if not animation.frames:
            raise ValueError(f'{animation.name} has no frames')
        if not isfinite(animation.frame_interval) or animation.frame_interval <= 0:
            raise ValueError(f'{animation.name} has an invalid frame interval')
        for frame in animation.frames:
            if frame.left < 0 or frame.top < 0:
                raise ValueError(f'{animation.name} has a negative frame origin')
            if frame.left + frame.width > SHEET_WIDTH:
                raise ValueError(f'{animation.name} exceeds the sprite sheet width')
            if frame.top + frame.height > SHEET_HEIGHT:
                raise ValueError(f'{animation.name} exceeds the sprite sheet height')


def next_animation_index(current: int) -> int:
    if not ANIMATIONS:
        raise ValueError('at least one animation is required')
    if not 0 <= current < len(ANIMATIONS):
        raise IndexError('animation index is out of range')
    return (current + 1) % len(ANIMATIONS)


if __name__ == '__main__':
    main()
