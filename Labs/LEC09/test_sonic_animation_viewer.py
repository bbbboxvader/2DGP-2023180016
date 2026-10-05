import unittest
from types import SimpleNamespace
from unittest.mock import patch

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


class ViewerIntegrationTests(unittest.TestCase):
    def test_all_first_frames_are_centered_and_scaled_without_distortion(self):
        class Sprite:
            def __init__(self):
                self.calls = []

            def clip_draw(self, *args):
                self.calls.append(args)

        sprite = Sprite()
        with patch.object(viewer, 'clear_canvas') as clear_canvas:
            with patch.object(viewer, 'update_canvas') as update_canvas:
                for animation in viewer.ANIMATIONS:
                    viewer.draw_frame(sprite, animation, 0)

        self.assertEqual(len(sprite.calls), len(viewer.ANIMATIONS))
        self.assertEqual(clear_canvas.call_count, len(viewer.ANIMATIONS))
        self.assertEqual(update_canvas.call_count, len(viewer.ANIMATIONS))
        for call in sprite.calls:
            _, _, source_width, source_height, center_x, center_y, draw_width, draw_height = call
            self.assertEqual(
                (center_x, center_y),
                (viewer.CANVAS_WIDTH // 2, viewer.CANVAS_HEIGHT // 2),
            )
            self.assertLessEqual(draw_width, viewer.CANVAS_WIDTH - 2 * viewer.CANVAS_MARGIN)
            self.assertLessEqual(draw_height, viewer.CANVAS_HEIGHT - 2 * viewer.CANVAS_MARGIN)
            self.assertAlmostEqual(draw_width / draw_height, source_width / source_height, delta=0.06)

    def test_every_scaled_frame_fits_the_centered_canvas(self):
        for animation in viewer.ANIMATIONS:
            for frame in animation.frames:
                width, height = viewer.scaled_frame_size(frame)
                self.assertLessEqual(width, viewer.CANVAS_WIDTH - 2 * viewer.CANVAS_MARGIN)
                self.assertLessEqual(height, viewer.CANVAS_HEIGHT - 2 * viewer.CANVAS_MARGIN)

    def test_window_close_and_escape_are_recognized(self):
        close_event = SimpleNamespace(type=viewer.SDL_QUIT)
        escape_event = SimpleNamespace(type=viewer.SDL_KEYDOWN, key=viewer.SDLK_ESCAPE)
        with patch.object(viewer, 'get_events', return_value=[close_event]):
            self.assertTrue(viewer.should_quit())
        with patch.object(viewer, 'get_events', return_value=[escape_event]):
            self.assertTrue(viewer.should_quit())
        with patch.object(viewer, 'get_events', return_value=[]):
            self.assertFalse(viewer.should_quit())

    def test_main_closes_canvas_when_asset_loading_fails(self):
        with patch.object(viewer, 'open_canvas') as open_canvas:
            with patch.object(viewer, 'load_image', side_effect=FileNotFoundError):
                with patch.object(viewer, 'close_canvas') as close_canvas:
                    with self.assertRaises(FileNotFoundError):
                        viewer.main()
        open_canvas.assert_called_once_with(viewer.CANVAS_WIDTH, viewer.CANVAS_HEIGHT)
        close_canvas.assert_called_once_with()

    def test_main_renders_the_current_animation_frame(self):
        with patch.object(viewer, 'open_canvas'):
            with patch.object(viewer, 'close_canvas'):
                with patch.object(viewer, 'load_image'):
                    with patch.object(viewer, 'get_time', side_effect=(0.0, 0.1)):
                        with patch.object(
                            viewer,
                            'get_events',
                            side_effect=([], [SimpleNamespace(type=viewer.SDL_QUIT)]),
                        ):
                            with patch.object(viewer, 'draw_frame') as draw_frame:
                                with patch.object(viewer, 'delay'):
                                    viewer.main()

        self.assertEqual(draw_frame.call_count, 1)
        self.assertEqual(len(draw_frame.call_args.args), 3)
        self.assertIs(draw_frame.call_args.args[1], viewer.ANIMATIONS[0])
        self.assertEqual(draw_frame.call_args.args[2], 1)


if __name__ == '__main__':
    unittest.main()
