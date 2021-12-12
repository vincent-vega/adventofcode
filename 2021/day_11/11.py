#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import lru_cache
from itertools import count


@lru_cache(maxsize=128)
def _adjacent(x: int, y: int) -> set:
    return { (x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0) }


def _increment(octopus: dict, x: int, y: int) -> int:
    flashes = 0
    octopus[x, y] += 1
    if octopus[x, y] == 10:
        flashes += 1
        for xx, yy in filter(lambda c: c in octopus, _adjacent(x, y)):
            flashes += _increment(octopus, xx, yy)
    return flashes


def _normalize(octopus: dict) -> dict:
    return { k: 0 if v > 9 else v for k, v in octopus.items() }


def part1(octopus: dict, cnt: int) -> int:
    X, Y = max(map(lambda x: x[0], octopus)) + 1, max(map(lambda x: x[1], octopus)) + 1
    flashes = 0
    for _ in range(cnt):
        flashes += sum(_increment(octopus, x, y) for y in range(Y) for x in range(X))
        octopus = _normalize(octopus)
    return flashes


def part2(octopus: dict) -> int:
    X, Y = max(map(lambda x: x[0], octopus)) + 1, max(map(lambda x: x[1], octopus)) + 1
    for n in count(1):
        if len(octopus) == sum(_increment(octopus, x, y) for y in range(Y) for x in range(X)):
            return n
        octopus = _normalize(octopus)


if __name__ == '__main__':
    with open('input.txt') as f:
        octopus = { (x, y): n for y, line in enumerate(f.read().splitlines()) for x, n in enumerate(map(int, line)) }
    print(part1(dict(octopus), 100))  # 1694
    print(part2(octopus))  # 346
