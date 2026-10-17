"""Larger stock Tulip launcher; tested with the 2026-10-14 firmware.

Uses the existing ui launcher and actions. No copied upstream implementation.
Install in /user/lib and call apply() from /user/boot.py.
"""

import ui
import lvgl as lv


def _font():
    for size in (24, 20, 16, 12):
        font = getattr(lv, "font_montserrat_%d" % size, None)
        if font is not None:
            return font


def _resize_menu():
    menu = ui.lv_launcher
    if menu is None:
        return
    menu.set_size(340, 480)
    menu.align(lv.ALIGN.BOTTOM_RIGHT, -12, -88)
    menu.set_style_text_font(_font(), 0)
    for index in range(menu.get_child_count()):
        row = menu.get_child(index)
        row.set_height(52)
        row.set_style_min_height(52, 0)
        row.set_flex_grow(0)
        row.set_style_text_font(_font(), 0)
        row.set_style_pad_left(16, 0)
        row.set_style_pad_right(16, 0)


def _launcher(event=True):
    _original_launcher(event)
    _resize_menu()


def _resize_button(screen):
    if screen.name != "repl":
        return
    button = screen.launcher_button
    button.set_size(96, 72)
    button.align(lv.ALIGN.BOTTOM_RIGHT, -12, -12)
    label = button.get_child(0)
    label.set_text("Menu")
    label.set_style_text_font(_font(), 0)
    label.center()
    button.remove_event_cb(_original_launcher)
    button.remove_event_cb(_launcher)
    button.add_event_cb(_launcher, lv.EVENT.CLICKED, None)


def _draw_task_bar(screen):
    _original_draw_task_bar(screen)
    _resize_button(screen)


def apply():
    global _original_launcher, _original_draw_task_bar
    if getattr(ui, "_large_menu_installed", False):
        return
    _original_launcher = ui.launcher
    _original_draw_task_bar = ui.UIScreen.draw_task_bar
    _resize_button(ui.repl_screen)
    ui.launcher = _launcher
    ui.UIScreen.draw_task_bar = _draw_task_bar
    ui._large_menu_installed = True
    _resize_menu()
