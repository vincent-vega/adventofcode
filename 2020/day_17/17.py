#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter
from itertools import combinations


def _deltas(size: int, cache: dict={}) -> set:
    if 'deltas' in cache:
        return cache['deltas']
    zero_delta = (0,) * size
    cache['deltas'] = { c for c in combinations([-1, 0, 1] * size, size) if c != zero_delta }
    return cache['deltas']


def _neighbors(coord: tuple, cache: dict={}) -> set:
    if coord in cache:
        return cache[coord]
    cache[coord] = { tuple(map(lambda c, d: c - d, coord, delta)) for delta in _deltas(len(coord), cache) }
    return cache[coord]


def _cycle(cubes: dict, rounds: int=6) -> dict:
    cache = {}
    for _ in range(rounds):
        nxt = {}
        cubes_freq = Counter([ cc for c in cubes.keys() for cc in _neighbors(c, cache) ])
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
