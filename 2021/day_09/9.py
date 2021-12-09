#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque
from functools import reduce


def _low(heightmap: list, x: int, y: int) -> bool:
    X, Y = len(heightmap[0]), len(heightmap)
    n = heightmap[y][x]
    if x - 1 >= 0 and heightmap[y][x - 1] <= n:
        return False
    if x + 1 < X and heightmap[y][x + 1] <= n:
        return False
    if y - 1 >= 0 and heightmap[y - 1][x] <= n:
        return False
    if y + 1 < Y and heightmap[y + 1][x] <= n:
        return False
    return True


def _low_points(heightmap: list) -> set:
    X, Y = len(heightmap[0]), len(heightmap)
    return { (x, y) for y in range(Y) for x in range(X) if _low(heightmap, x, y) }


def part1(heightmap: list) -> int:
    return sum(heightmap[y][x] + 1 for x, y in _low_points(heightmap))


def _adj(x: int, y: int, X: int, Y: int) -> set:
    adj = { (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1) }
    return set(filter(lambda c: c[0] >= 0 and c[0] < X and c[1] >= 0 and c[1] < Y, adj))


def _basin(heightmap: list, x: int, y: int) -> int:
    X, Y = len(heightmap[0]), len(heightmap)
    size = 1
    D = deque(_adj(x, y, X, Y))
    visited = { (x, y) }
    while D:
        x, y = D.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if heightmap[y][x] < 9:
            size += 1
            D.extend(_adj(x, y, X, Y))
    return size


def part2(heightmap: list) -> int:
    return reduce(lambda i, j: i * j, sorted([ _basin(heightmap, x, y) for x, y in _low_points(heightmap) ], reverse=True)[:3])


if __name__ == '__main__':
    with open('input.txt') as f:
        heightmap = [ list(map(int, line)) for line in f.read().splitlines() ]
    print(part1(heightmap))  # 633
    print(part2(heightmap))  # 1050192
