"""Host checks for note lifecycle; no hardware/audio claims."""
import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch


class TouchNotes(unittest.TestCase):
    def setUp(self):
        self.events = []
        self.synths = {
            ch: SimpleNamespace(
                note_on=lambda n, v, ch=ch: self.events.append((ch, 'on', n)),
                note_off=lambda n, ch=ch: self.events.append((ch, 'off', n)))
            for ch in (1, 2)
        }
        self.app = SimpleNamespace(
            piano_x=112, piano_y=330, piano_w=798, piano_h=270,
            white_key_w=57, black_key_w=38, black_key_h=180,
            black_key_starts=[148, 217, 315, 381, 447, 542, 612, 711, 776, 843],
            channels=SimpleNamespace(selected=0), held_note={})
        self.coords = (120, 550, -1, -1, -1, -1)
        modules = {
            'tulip': SimpleNamespace(touch=lambda: self.coords),
            'voices': SimpleNamespace(app=self.app),
            'midi': SimpleNamespace(config=SimpleNamespace(get_synth=self.synths.get))}
        spec = importlib.util.spec_from_file_location(
            'voices_touch_test', Path(__file__).with_name('voices_touch.py'))
        self.fix = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, modules):
            spec.loader.exec_module(self.fix)

    def test_slide_releases_previous_note_and_final_release_clears_all(self):
        self.fix.touch(0)
        self.coords = (180, 550, -1, -1, -1, -1)
        self.fix.touch(0)
        self.fix.touch(1)
        self.assertEqual(self.events, [(1, 'on', 48), (1, 'off', 48),
                                       (1, 'on', 50), (1, 'off', 50)])
        self.assertEqual(self.app.held_note, {})

    def test_partial_chord_release_and_repeated_samples(self):
        self.coords = (120, 550, 180, 550, -1, -1)
        self.fix.touch(0)
        self.fix.touch(0)
        self.assertEqual(len(self.events), 2)
        self.coords = (180, 550, -1, -1, -1, -1)
        self.fix.touch(0)
        self.assertEqual(self.events[-1], (1, 'off', 48))
        self.fix.touch(1)
        self.assertEqual(self.events[-1], (1, 'off', 50))

    def test_channel_switch_releases_original_synth(self):
        self.fix.touch(0)
        self.app.channels.selected = 1
        self.fix.touch(0)
        self.assertEqual(self.events, [(1, 'on', 48), (1, 'off', 48), (2, 'on', 48)])

    def test_leaving_keyboard_and_right_boundary(self):
        self.fix.touch(0)
        self.coords = (910, 550, -1, -1, -1, -1)
        self.fix.touch(0)
        self.assertEqual(self.events[-1], (1, 'off', 48))
        self.assertEqual(self.app.held_note, {})


if __name__ == '__main__':
    unittest.main()
