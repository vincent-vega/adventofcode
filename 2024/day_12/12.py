#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from common.lib import _print, _adj


def _regions(garden: dict[tuple[int], str]):
    seen = set()
    regions = defaultdict(set)
    for x, y in ((x, y) for x, y in garden if (x, y) not in seen):
        region_id = len(regions)
        R = [ (x, y) ]
        while R:
            cur = R.pop()
            seen.add(cur)
            regions[region_id].add(cur)
            for i, j in ((i, j) for i, j in _adj(*cur) if (i, j) in garden and garden[i, j] == garden[x, y] and (i, j) not in seen):
                R.append((i, j))
    return regions


def _perimeter(region: set[tuple[int]]) -> int:
    return sum(1 for x, y in region for i, j in _adj(x, y) if (i, j) not in region)


def part1(garden: dict[tuple[int], str]) -> int:
    regions = _regions(garden)
    return sum(len(r) * _perimeter(r) for r in regions.values())


def _sides(region: set[tuple[int]]) -> int:
    # sides = { for r in regions for x, y in _adj(*r) }
    pass


def part2(garden: dict[tuple[int], str]) -> int:
    regions = _regions(garden)
    return sum(len(r) * _sides(r) for r in regions.values())


# import pudb; pu.db
if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.read().splitlines()
        # X = len(lines[0]) - 1
        # Y = len(lines) - 1
        garden = { (x, y): c for y, line in enumerate(lines) for x, c in enumerate(line) }
    # print(part1(garden, (X, Y)))  # 1415378
    assert part1(garden) == 1415378
    # _print(part2(garden))  #
