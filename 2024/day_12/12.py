#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from common.lib import _adj


def _regions(garden: dict[tuple[int], str]) -> dict[int, set[tuple[int]]]:
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


def _corners(x: int, y: int, region: set[tuple[int]]) -> int:
    return sum(((x + dx, y) not in region and (x, y + dy) not in region) or ((x + dx, y) in region and (x, y + dy) in region and (x + dx, y + dy) not in region) for dx in (1, -1) for dy in (1, -1))


def _sides(region: set[tuple[int]]) -> int:
    return sum(_corners(*coord, region - { coord }) for coord in region)


def part2(garden: dict[tuple[int], str]) -> int:
    regions = _regions(garden)
    return sum(len(r) * _sides(r) for r in regions.values())


if __name__ == '__main__':
    with open('input.txt') as f:
        garden = { (x, y): c for y, line in enumerate(f.read().splitlines()) for x, c in enumerate(line) }
    print(part1(garden))  # 1415378
    print(part2(garden))  # 862714
