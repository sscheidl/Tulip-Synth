"""Collect five touch points without changing calibration or boot settings."""

import lvgl as lv
import tulip
import ui
import time

samples = []
targets = [(120, 100), (904, 100), (512, 300), (120, 500), (904, 500)]
old_calibration = None
screen = None
index = 0
last_release = 0


def _draw(_=None):
    if index >= len(targets):
        marker.add_flag(lv.obj.FLAG.HIDDEN)
        message.set_text("Messung fertig. Bitte im Chat warten.")
        return
    x, y = targets[index]
    marker.set_pos(x - 24, y - 24)
    message.set_text("Punkt %d / 5: Kreuz einmal mittig antippen" % (index + 1))


def _released(event):
    global index, last_release
    now = time.ticks_ms()
    if index >= len(targets) or time.ticks_diff(now, last_release) < 350:
        return
    last_release = now
    x, y = tulip.touch()[:2]
    if x < 0 or y < 0:
        return
    samples.append((targets[index][0], targets[index][1], x, y))
    print("CAL_SAMPLE", samples[-1])
    index += 1
    tulip.defer(_draw, None, 150)


def start():
    global screen, marker, message, index, samples, old_calibration, last_release
    samples = []
    index = 0
    last_release = time.ticks_ms() - 1000
    old_calibration = tulip.touch_delta()
    screen = ui.UIScreen("touch_calibration", bg_color=0)
    screen.hide_task_bar = True
    screen.group.remove_flag(lv.obj.FLAG.SCROLLABLE)
    screen.group.add_flag(lv.obj.FLAG.CLICKABLE)
    screen.group.add_event_cb(_released, lv.EVENT.RELEASED, None)
    message = lv.label(screen.group)
    message.set_style_text_font(lv.font_montserrat_24, 0)
    message.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
    message.set_width(940)
    message.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
    message.set_pos(42, 200)
    marker = lv.obj(screen.group)
    marker.set_size(48, 48)
    marker.remove_flag(lv.obj.FLAG.CLICKABLE)
    marker.remove_flag(lv.obj.FLAG.SCROLLABLE)
    marker.set_style_radius(24, 0)
    marker.set_style_bg_color(lv.color_hex(0xFFD54F), 0)
    marker.set_style_border_width(0, 0)
    cross = lv.label(marker)
    cross.set_text("+")
    cross.set_style_text_font(lv.font_montserrat_36, 0)
    cross.set_style_text_color(lv.color_hex(0x000000), 0)
    cross.center()
    _draw()
    screen.present()


def close():
    if screen is not None:
        screen.screen_quit_callback(None)
