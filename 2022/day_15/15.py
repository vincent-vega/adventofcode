#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re


def _manh(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1 - y2)


def part1(positions: tuple[int, int, int, int], row: int) -> int:
    locations = set()
    others = set()
    for sx, sy, bx, by in positions:
        d = _manh(sx, sy, bx, by)
        if sy == row:
            others.add(sx)
        if by == row:
            others.add(bx)
        if (dx := d - abs(row - sy)) > -1:
            locations.update(x for x in range(sx - dx, sx + dx + 1))
    return len(locations - others)


def _out_of_scope(sx: int, sy: int, bx: int, by: int, M: int) -> set[tuple[int, int]]:
    '''
    Return every position whose distance from the sensor is radius + 1
    '''
    d = _manh(sx, sy, bx, by) + 1
    p = set()
    for dx in filter(lambda dx: 0 <= sx + dx <= M, range(-1 * d, d + 1)):
        x = sx + dx
        dy = d - abs(dx)
        if dy > 0:
            if 0 <= sy + dy <= M:
                p.add((x, (sy + dy)))
            if 0 <= sy - dy <= M:
                p.add((x, (sy - dy)))
        elif 0 <= sy <= M:
            p.add((x, sy))
    return p


def part2(positions: tuple[int, int, int, int], M: int) -> int:
    for i, (sx1, sy1, bx1, by1) in enumerate(positions):
        for x, y in _out_of_scope(sx1, sy1, bx1, by1, M):
            for _, (sx2, sy2, bx2, by2) in filter(lambda e: e[0] != i, enumerate(positions)):
                s2_d = _manh(x, y, sx2, sy2)  # distance between the current position and the (other) sensor
                s2_radius = _manh(sx2, sy2, bx2, by2)  # radius scanned by the (other) sensor
                if s2_d <= s2_radius:
                    break
            else:
                return x * 4_000_000 + y
    return -1


if __name__ == '__main__':
    with open('input.txt') as f:
        positions = [ tuple(map(int, re.findall(r'-?\d+', line))) for line in f.read().splitlines() ]
    print(part1(positions, 2_000_000))  # 5256611
    print(part2(positions, 4_000_000))  # 13337919186981
