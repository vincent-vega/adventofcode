#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter
from functools import lru_cache
from itertools import combinations


@lru_cache(maxsize=None)
def _deltas(size: int) -> set:
    zero_delta = (0,) * size
    return { c for c in combinations([-1, 0, 1] * size, size) if c != zero_delta }


@lru_cache(maxsize=None)
def _neighbors(coord: tuple) -> set:
    return { tuple(map(lambda c, d: c - d, coord, delta)) for delta in _deltas(len(coord)) }


def _cycle(cubes: dict, rounds: int=6) -> dict:
    for _ in range(rounds):
        nxt = {}
        cubes_freq = Counter([ cc for c in cubes.keys() for cc in _neighbors(c) ])
        for coord, neigh in cubes_freq.items():
            active = cubes.get(coord)
            if active and (neigh == 2 or neigh == 3):
                nxt[coord] = True
            elif not active and neigh == 3:
                nxt[coord] = True
        cubes = nxt
    return cubes


if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.read().splitlines()
        cubes = { (0, y, x): True for y in range(len(lines)) for x, s in enumerate(lines[y]) if s == '#' }
    print(len(_cycle(cubes)))  # 295
    print(len(_cycle({ (0, *c): True for c in cubes })))  # 1972
