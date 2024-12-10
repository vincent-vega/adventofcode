#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce
from typing import Generator


def _gps(delta: tuple[int, int], limit: tuple[int, int]) -> Generator[tuple, None, None]:
    max_x, max_y = limit
    delta_x, delta_y = delta
    x, y = 0, 0
    while y <= max_y:
        x, y = (x + delta_x) % max_x, y + delta_y
        yield x, y


def _count_trees(world: dict, delta: tuple[int, int], map_size: tuple[int, int]) -> int:
    return sum([ 1 for (x, y) in _gps(delta, map_size) if world.get((x, y)) ])


def part1(world: dict, map_size: tuple[int, int]) -> int:
    return _count_trees(world, (3, 1), map_size)


def part2(world: dict, map_size: tuple[int, int]) -> int:
    slopes = [ (1, 1), (3, 1), (5, 1), (7, 1), (1, 2) ]
    return reduce(lambda acc, x: acc * x, [ _count_trees(world, slope, map_size) for slope in slopes ])


if __name__ == '__main__':
    W = {}
    with open('input.txt') as f:
        y = 0
        for line in f:
            max_x = len(line.strip())
            for coord in [ (x, y) for x in range(len(line)) if line[x] == '#' ]:
                W[coord] = True
            y += 1
    _, max_y = max(W.keys(), key=lambda k: k[1])
    print(part1(W, (max_x, max_y)))  # 181
    print(part2(W, (max_x, max_y)))  # 1260601650
