#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import combinations


def _manhattan(g1: tuple[int], g2: tuple[int]) -> int:
    g1x, g1y = g1
    g2x, g2y = g2
    return abs(g1x - g2x) + abs(g1y - g2y)


def _cnt(space: set[int], limit: int) -> int:
    return sum(1 for s in space if s < limit)


def _expand(galaxies: set[tuple[int]], n: int = 1) -> set[tuple[int]]:
    X = { gx for gx, _ in galaxies }
    Y = { gy for _, gy in galaxies }
    space_x = { x for x in range(max(X)) if x not in X }
    space_y = { y for y in range(max(Y)) if y not in Y }
    return { (x + n * _cnt(space_x, x), y + n * _cnt(space_y, y)) for x, y in galaxies }


def part1(galaxies: set[tuple[int]]) -> int:
    return sum(_manhattan(g1, g2) for g1, g2 in combinations(_expand(galaxies), 2))


def part2(galaxies: set[tuple[int]]) -> int:
    return sum(_manhattan(g1, g2) for g1, g2 in combinations(_expand(galaxies, 10**6 - 1), 2))


if __name__ == '__main__':
    with open('input.txt') as f:
        galaxies = { (x, y) for y, line in enumerate(f.read().splitlines()) for x, c in enumerate(line) if c == '#' }
    print(part1(galaxies))  # 9947476
    print(part2(galaxies))  # 519939907614
