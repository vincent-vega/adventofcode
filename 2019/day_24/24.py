#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter
from math import pow


def _infected(was_infected: bool, neighbour_cnt: int) -> bool:
    if neighbour_cnt == 1:
        return True
    return not was_infected and neighbour_cnt == 2


def _near_2D(x: int, y: int) -> tuple:
    return tuple((x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if abs(dx) != abs(dy) and -1 < x + dx < 5 and -1 < y + dy < 5)


def _near_3D(level: int, x: int, y: int) -> tuple:
    assert (x, y) != (2, 2), "Invalid coordinate"
    near = [ (level, xx, yy) for xx, yy in _near_2D(x, y) if (xx, yy) != (2, 2) ]
    # inner
    if (x, y) == (2, 1):
        return tuple(near + [ (level + 1, xx, 0) for xx in range(5) ])
    if (x, y) == (2, 3):
        return tuple(near + [ (level + 1, xx, 4) for xx in range(5) ])
    if (x, y) == (1, 2):
        return tuple(near + [ (level + 1, 0, yy) for yy in range(5) ])
    if (x, y) == (3, 2):
        return tuple(near + [ (level + 1, 4, yy) for yy in range(5) ])
    # outer
    if x == 0:
        near.append((level - 1, 1, 2))
    if y == 0:
        near.append((level - 1, 2, 1))
    if x == 4:
        near.append((level - 1, 3, 2))
    if y == 4:
        near.append((level - 1, 2, 3))
    return tuple(near)


def _snapshot(M: set) -> tuple:
    return tuple(sorted(M))


def _parse_line(line: str) -> tuple:
    return tuple(x for x in range(len(line)) if line[x] == '#')


def _next_2D(M: set) -> set:
    freq = Counter(c for x, y in M for c in _near_2D(x, y))
    return { (x, y) for (x, y), n in freq.items() if _infected((x, y) in M, n) }


def _next_3D(M: set) -> set:
    freq = Counter(c for lvl, x, y in M for c in _near_3D(lvl, x, y))
    return { (lvl, x, y) for (lvl, x, y), n in freq.items() if _infected((lvl, x, y) in M, n) }


def part1(M: set) -> int:
    history = set()
    state = _snapshot(M)
    while state not in history:
        history.add(state)
        M = _next_2D(M)
        state = _snapshot(M)
    return sum(int(pow(2, x + 5 * y)) for x, y in M)


def part2(M: set) -> int:
    M = { (0, x, y) for x, y in M }
    for _ in range(200):
        M = _next_3D(M)
    return len(M)


if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.read().splitlines()
    M = { (x, y) for y in range(len(lines)) for x in _parse_line(lines[y]) }
    print(part1(M))  # 28778811
    print(part2(M))  # 2097
