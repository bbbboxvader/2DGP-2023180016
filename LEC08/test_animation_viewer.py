import unittest

from animation_viewer import (
    ACTIONS,
    FRAME_SIZE,
    SHEET_HEIGHT,
    SHEET_WIDTH,
    advance_frame,
    frame_rect,
)


class AnimationDataTest(unittest.TestCase):
    def test_has_at_least_four_animations(self):
        self.assertGreaterEqual(len(ACTIONS), 4)

    def test_animations_use_different_frame_counts(self):
        frame_counts = {action.frame_count for action in ACTIONS}
        self.assertGreaterEqual(len(frame_counts), 2)

    def test_all_frames_stay_inside_sprite_sheet(self):
        for action in ACTIONS:
            for frame in range(action.frame_count):
                left, bottom, width, height = frame_rect(action.row, frame)
                self.assertGreaterEqual(left, 0)
                self.assertGreaterEqual(bottom, 0)
                self.assertLessEqual(left + width, SHEET_WIDTH)
                self.assertLessEqual(bottom + height, SHEET_HEIGHT)
                self.assertEqual((width, height), (FRAME_SIZE, FRAME_SIZE))

    def test_last_frame_advances_to_next_action(self):
        last_frame = ACTIONS[0].frame_count - 1
        self.assertEqual(advance_frame(0, last_frame), (1, 0))

    def test_last_action_wraps_to_first_action(self):
        last_action = len(ACTIONS) - 1
        last_frame = ACTIONS[last_action].frame_count - 1
        self.assertEqual(advance_frame(last_action, last_frame), (0, 0))


if __name__ == '__main__':
    unittest.main()
