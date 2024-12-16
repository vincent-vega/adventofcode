#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
from functools import reduce
import re


def _move(robots: list[tuple[int]], X: int, Y: int) -> list[tuple[int]]:
    return [ ((x + vx) % X, (y + vy) % Y, vx, vy) for x, y, vx, vy in robots ]


def _count(robots: list[tuple[int]], X: int, Y: int, quadrant: int) -> int:
    X = X // 2
    Y = Y // 2
    if quadrant == 0:
        return sum([ 1 for x, y, _, __ in robots if x < X and y < Y ])
    elif quadrant == 1:
        return sum([ 1 for x, y, _, __ in robots if x > X and y < Y ])
    elif quadrant == 2:
        return sum([ 1 for x, y, _, __ in robots if x < X and y > Y ])
    elif quadrant == 3:
        return sum([ 1 for x, y, _, __ in robots if x > X and y > Y ])
    raise Exception('Invalid quadrant')


def part1(robots: list[tuple[int]], X: int, Y: int) -> int:
    for _ in range(100):
        robots = _move(robots, X, Y)
    return reduce(lambda a, b: a * b, [ _count(robots, X, Y, quadrant) for quadrant in range(4) ])


def _render(robots: list[tuple[int]], N: int, X: int, Y: int):
    robots = { (x, y) for x, y, _, __ in robots }
    img = Image.new('1', (X, Y), color=0)
    for x, y in ((x, y) for x in range(X) for y in range(Y) if (x, y) in robots):
        img.putpixel((x, y), 1)
    img.save(f'{N}.png')


def part2(robots: list[tuple[int]], X: int, Y: int, seconds: int):
    for _ in range(seconds):
        robots = _move(robots, X, Y)
    _render(robots, seconds, X, Y)


if __name__ == '__main__':
    with open('input.txt') as f:
        robots = [ tuple(map(int, re.findall(r'-?\d+', line))) for line in f ]
    print(part1(robots, 101, 103))  # 216772608
    part2(robots, 101, 103, 6888)  # 6888
