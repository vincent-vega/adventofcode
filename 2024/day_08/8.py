#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from common.lib import _manhattan
from itertools import combinations


def _aligned(a: tuple[int, int], b: tuple[int, int], c: tuple[int, int]) -> bool:
    xa, ya = a
    xb, yb = b
    xc, yc = c
    return (xb - xa) * (yc - ya) == (yb - ya) * (xc - xa)  # (xb - xa) / (xc - xa) == (yb - ya) / (yc - ya)


def _antinodes(antennas: dict[str, set[tuple[int, int]]], limit: tuple[int, int], res_harm: bool = False) -> set[tuple[int, int]]:
    X, Y = limit
    antinodes = set()
    for freq, ant in antennas.items():
        couples = list(combinations(ant, 2))
        for x in range(X + 1):
            for y in filter(lambda y: (x, y) not in antinodes, range(Y + 1)):
                for c1, c2 in couples:
                    if _aligned((x, y), c1, c2):
                        if res_harm or _manhattan(x, y, *c1) == 2 * _manhattan(x, y, *c2) or 2 * _manhattan(x, y, *c1) == _manhattan(x, y, *c2):
                            antinodes.add((x, y))
    return antinodes


def part1(antennas: dict[str, set[tuple[int, int]]], limit: tuple[int, int]) -> int:
    return len(_antinodes(antennas, limit))


def part2(antennas: dict[str, set[tuple[int, int]]], limit: tuple[int, int]) -> int:
    return len(_antinodes(antennas, limit, True))


if __name__ == '__main__':
    antennas = defaultdict(set)
    with open('input.txt') as f:
        lines = f.read().splitlines()
        X = len(lines[0]) - 1
        Y = len(lines) - 1
        for y, line in enumerate(lines):
            for x, freq in ((x, freq) for x, freq in enumerate(line) if freq != '.'):
                antennas[freq].add((x, y))
    print(part1(antennas, (X, Y)))  # 409
    print(part2(antennas, (X, Y)))  # 1308
