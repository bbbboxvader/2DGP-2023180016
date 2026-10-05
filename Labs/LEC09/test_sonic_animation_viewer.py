import unittest

import sonic_animation_viewer as viewer


class AnimationDataTests(unittest.TestCase):
    def test_all_nine_sequences_have_frames(self):
        self.assertEqual(len(viewer.ANIMATIONS), 9)
        self.assertTrue(all(animation.frames for animation in viewer.ANIMATIONS))

    def test_sequences_use_different_frame_counts_and_cadences(self):
        self.assertGreater(len({len(action.frames) for action in viewer.ANIMATIONS}), 1)
        self.assertGreater(len({action.frame_interval for action in viewer.ANIMATIONS}), 1)

    def test_all_frame_rectangles_fit_the_sheet(self):
        viewer.validate_frame_bounds()
        for animation in viewer.ANIMATIONS:
            for frame in animation.frames:
                left, bottom, width, height = viewer.pico_frame_rect(frame)
                self.assertGreaterEqual(left, 0)
                self.assertGreaterEqual(bottom, 0)
                self.assertLessEqual(left + width, viewer.SHEET_WIDTH)
                self.assertLessEqual(bottom + height, viewer.SHEET_HEIGHT)

    def test_png_top_coordinate_converts_to_pico_bottom_coordinate(self):
        frame = viewer.Frame(12, 34, 20, 10)
        self.assertEqual(viewer.pico_frame_rect(frame), (12, 481, 20, 10))

    def test_animation_order_wraps_and_rejects_invalid_indices(self):
        self.assertEqual(viewer.next_animation_index(0), 1)
        self.assertEqual(viewer.next_animation_index(len(viewer.ANIMATIONS) - 1), 0)
        with self.assertRaises(IndexError):
            viewer.next_animation_index(len(viewer.ANIMATIONS))


class PlaybackTimelineTests(unittest.TestCase):
    def test_frame_advance_reports_cycle_completion(self):
        state = viewer.PlaybackState()
        self.assertFalse(viewer.advance_frame(state))
        state.frame_index = len(viewer.ANIMATIONS[0].frames) - 1
        self.assertTrue(viewer.advance_frame(state))
        self.assertEqual(state.frame_index, 0)

    def test_fifth_cycle_schedules_exactly_one_second(self):
        state = viewer.PlaybackState()
        for cycle in range(4):
            self.assertFalse(viewer.record_completed_cycle(state, float(cycle)))
        self.assertTrue(viewer.record_completed_cycle(state, 4.0))
        self.assertEqual(state.wait_until, 5.0)
        self.assertEqual(state.completed_cycles, 5)

    def test_wait_does_not_transition_early(self):
        state = viewer.PlaybackState(completed_cycles=5, wait_until=2.0)
        self.assertFalse(viewer.advance_timeline(state, 1.999))
        self.assertEqual(state.animation_index, 0)
        self.assertTrue(viewer.advance_timeline(state, 2.0))
        self.assertEqual(state.animation_index, 1)
        self.assertEqual(state.completed_cycles, 0)

    def test_every_sequence_repeats_five_times_then_wraps(self):
        state = viewer.PlaybackState(
            next_frame_at=viewer.ANIMATIONS[0].frame_interval,
        )
        transitions = []
        for expected_index, animation in enumerate(viewer.ANIMATIONS):
            self.assertEqual(state.animation_index, expected_index)
            for _ in range(len(animation.frames) * viewer.REPEATS_PER_ANIMATION):
                self.assertTrue(viewer.advance_timeline(state, state.next_frame_at))
            self.assertEqual(state.completed_cycles, viewer.REPEATS_PER_ANIMATION)
            self.assertEqual(state.frame_index, len(animation.frames) - 1)
            self.assertIsNotNone(state.wait_until)
            deadline = state.wait_until
            self.assertFalse(viewer.advance_timeline(state, deadline - 0.001))
            self.assertEqual(state.animation_index, expected_index)
            self.assertTrue(viewer.advance_timeline(state, deadline))
            transitions.append(state.animation_index)
        expected_transitions = list(range(1, len(viewer.ANIMATIONS))) + [0]
        self.assertEqual(transitions, expected_transitions)


if __name__ == '__main__':
    unittest.main()