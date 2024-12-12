#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from common.lib import _print, _adj


def _regions(garden: dict[tuple[int], str], limit: tuple[int]):
    X, Y = limit
    g_seen = set()
    regions = defaultdict(set)
    for x, y in ((x, y) for x in range(X + 1) for y in range(Y + 1) if (x, y) not in g_seen):
        cur_r = garden[x, y]
        r_seen = {(x, y)}
        idx = len(regions)
        R = [(x, y)]
        while R:
            cur = R.pop()
            g_seen.add(cur)
            r_seen.add(cur)
            regions[idx].add(cur)
            for i, j in ((i, j) for i, j in _adj(*cur) if (i, j) in garden and (i, j) not in r_seen and garden[i, j] == cur_r):
                R.append((i, j))
    return regions


def _perimeter(region: set[tuple[int]]) -> int:
    return sum(1 for x, y in region for i, j in _adj(x, y) if (i, j) not in region)


def part1(garden: dict[tuple[int], str], limit: tuple[int]) -> int:
    regions = _regions(garden, limit)
    return sum(len(r) * _perimeter(r) for r in regions.values())


def _sides(region: set[tuple[int]]) -> int:
    # sides = { for r in regions for x, y in _adj(*r) }
    pass


def part2(garden: dict[tuple[int], str], limit: tuple[int]) -> int:
    regions = _regions(garden, limit)
    return sum(len(r) * _sides(r) for r in regions.values())


# import pudb; pu.db
if __name__ == '__main__':
    e = '''
AAAA
BBCD
BBCC
EEEC'''
    e = '''
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO'''
    lines = e.split()
    X = len(lines[0]) - 1
    Y = len(lines) - 1
    garden = { (x, y): c for y, line in enumerate(e.split()) for x, c in enumerate(line) }

    with open('input.txt') as f:
        lines = f.read().splitlines()
        X = len(lines[0]) - 1
        Y = len(lines) - 1
        garden = { (x, y): c for y, line in enumerate(lines) for x, c in enumerate(line) }
    # print(part1(garden, (X, Y)))  # 1415378
    assert part1(garden, (X, Y)) == 1415378
    # _print(part2(garden, (X, Y)))  #
