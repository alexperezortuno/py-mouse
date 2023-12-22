import argparse
import os
import sys
import keyboard

import mouse
from screeninfo import get_monitors, Monitor


def start(params: argparse.Namespace) -> None:
    m: Monitor = get_primary_screen()
    pos_x: int = m.width - 50
    pos_y: int = m.height - 50

    if params.screen is not None:
        monitors: list[Monitor] = get_all_monitors()
        pos_x = 0
        for m in monitors:
            print(f"Screen {m.name} found at {m.width}x{m.height}")
            pos_x += m.width - 50
        t = get_screen(params.screen)
        pos_y = t.height - 50

        print(f"Screen {params.screen} found at {pos_x}x{pos_y}")

    if params.move:
        try:
            wait_for_key('esc')
            while True:
                mouse.move(pos_x, pos_y, absolute=True, duration=0.2)
                mouse.move((pos_x + 5), pos_y, absolute=True, duration=0.2)
                mouse.move((pos_x + 5), (pos_y + 5), absolute=True, duration=0.2)
        except KeyboardInterrupt:
            print("Application closed")
            sys.exit(0)

    if params.all:
        get_all_monitors()
        sys.exit(0)

    if params.exists and get_screen(params.exists) is not None:
        print(f"Monitor {params.exists} exists")
        sys.exit(0)


def wait_for_key(key: str) -> None:
    keyboard.on_press_key(key, close_app)


def close_app(e):
    print('closing application...')
    os._exit(0)


def get_screen(name: str) -> Monitor | None:
    monitors: list[Monitor] = get_monitors()
    for m in monitors:
        if m.name.replace('\\\\.\\DISPLAY', '') == name:
            return m
    return None


def get_primary_screen() -> Monitor:
    monitors: list[Monitor] = get_monitors()
    for m in monitors:
        if m.is_primary:
            return m
    return monitors[0]


def get_all_monitors() -> list[Monitor]:
    return get_monitors()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PyMouse')
    parser.add_argument('--monitor', type=str, default='1', help='Monitor to be used')
    parser.add_argument('-a', '--all', help='Get all monitors', action='store_true')
    parser.add_argument('-e', '--exists', type=str, default=None, help='Check if monitor exists')
    parser.add_argument('-m', '--move', help='Move mouse', action='store_true')
    parser.add_argument('-p', '--position', help='Start at position', type=int, default=50)
    parser.add_argument('-s', '--screen', help='Screen', type=str, default=None)
    args = parser.parse_args()

    start(args)
