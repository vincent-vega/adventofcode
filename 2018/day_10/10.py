#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import namedtuple
import re

char_height = 10
Light = namedtuple('Light', [ 'x', 'y', 'vx', 'vy' ])


def _move(lights: list) -> list:
    return [ Light(x + vx, y + vy, vx, vy) for x, y, vx, vy in lights ]


def _delta_Y(lights: list) -> int:
    _, Y, *_ = max(lights, key=lambda light: light.y)
    _, y, *_ = min(lights, key=lambda light: light.y)
    return abs(Y - y)


def _message(lights: list) -> str:
    max_x, _, *_ = max(lights, key=lambda light: light.x)
    min_x, _, *_ = min(lights, key=lambda light: light.x)
    _, max_y, *_ = max(lights, key=lambda light: light.y)
    _, min_y, *_ = min(lights, key=lambda light: light.y)
    positions = { (x, y) for x, y, *_ in lights }
    return '\n'.join(''.join('#' if (x, y) in positions else '.' for x in range(min_x, max_x + 1)) for y in range(min_y, max_y + 1))


def part1(lights: list) -> str:
    while _delta_Y(lights) > char_height:
        lights = _move(lights)
    return _message(lights)


def part2(lights: list) -> int:
    seconds = 0
    while _delta_Y(lights) > char_height:
        lights = _move(lights)
        seconds += 1
    return seconds


if __name__ == '__main__':
    with open('input.txt') as f:
        lights = [ Light(*map(int, re.findall(r'-?\d+', line))) for line in f.read().splitlines() ]
    print(part1(lights))  # LCPGPXGL
    print(part2(lights))  # 10639
