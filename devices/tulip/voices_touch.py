"""Reconcile Voices touch notes on every sample, including slides and chords.

Personal runtime fix: import voices_touch; voices_touch.apply().
Uses the existing Voices layout and synth API; no upstream code copied.
"""

import tulip
import voices
import midi

_active = {}
_white = (0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23)
_black = (1, 3, 6, 8, 10, 13, 15, 18, 20, 22)


def _note(app, x, y):
    if not (app.piano_x <= x < app.piano_x + app.piano_w
            and app.piano_y <= y < app.piano_y + app.piano_h):
        return None
    if y < app.piano_y + app.black_key_h:
        for index, start in enumerate(app.black_key_starts):
            if start <= x < start + app.black_key_w:
                return 48 + _black[index]
    index = (x - app.piano_x) // app.white_key_w
    if 0 <= index < len(_white):
        return 48 + _white[index]
    return None


def _release():
    for key in list(_active):
        synth = _active[key]
        synth.note_off(key[1])
        del _active[key]
    voices.app.held_note = {}


def touch(up):
    app = voices.app
    wanted = set()
    channel = app.channels.selected + 1
    if not up:
        coords = tulip.touch()
        for index in range(0, 6, 2):
            note = _note(app, coords[index], coords[index + 1])
            if note is not None:
                wanted.add((channel, note))
    synth = midi.config.get_synth(channel)
    if synth is None:
        wanted.clear()
    # Keep the original synth for note-off, even after a channel/patch change.
    for key in list(_active):
        if key not in wanted or _active[key] is not synth:
            _active[key].note_off(key[1])
            del _active[key]
    for key in wanted:
        if key not in _active:
            synth.note_on(key[1], 1)
            _active[key] = synth
    app.held_note = {key[1]: True for key in _active}


def _activate(screen):
    _release()
    _original_activate(screen)
    tulip.touch_callback(touch)


def _deactivate(screen):
    _release()
    _original_deactivate(screen)


def _quit(screen):
    _release()
    _original_quit(screen)


def apply():
    global _original_activate, _original_deactivate, _original_quit
    if getattr(voices, '_touch_notes_fixed', False):
        return
    app = voices.app
    synth = midi.config.get_synth(app.channels.selected + 1)
    for note, held in app.held_note.items():
        if held:
            synth.note_off(note)
    app.held_note = {}
    _original_activate = voices.activate
    _original_deactivate = voices.deactivate
    _original_quit = voices.quit
    voices.activate = _activate
    voices.deactivate = _deactivate
    voices.quit = _quit
    app.activate_callback = _activate
    app.deactivate_callback = _deactivate
    app.quit_callback = _quit
    voices._touch_notes_fixed = True
    if app.active:
        tulip.touch_callback(touch)
