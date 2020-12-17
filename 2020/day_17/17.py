#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import combinations


def _neighbors(coord: tuple, cache: dict={}) -> set:
    if coord in cache:
        return cache[coord]
    zero_delta = (0,) * len(coord)
    deltas = { c for c in combinations([-1, 0, 1] * len(coord), len(coord)) if c != zero_delta }
    cache[coord] = { tuple( c - d for c, d in zip(coord, delta)) for delta in deltas }
    return cache[coord]


def _cycle(cubes: dict, cache: dict={}) -> dict:
    nxt = {}
    W = { cc for c in cubes.keys() for cc in _neighbors(c, cache) } | set(cubes.keys())
    for coord in W:
        active = cubes.get(coord)
        neigh = sum([ 1 for n in _neighbors(coord, cache) if cubes.get(n) ])
        if active and (neigh == 2 or neigh == 3):
            nxt[coord] = True
        elif not active and neigh == 3:
            nxt[coord] = True
    return nxt


def part1(cubes: dict, rounds: int=6) -> int:
    cache = {}
    for _ in range(rounds):
        cubes = _cycle(cubes, cache)
    return len(cubes.keys())


def part2(cubes: dict, rounds: int=6) -> int:
    cache = {}
    for _ in range(rounds):
        cubes = _cycle(cubes, cache)
    return len(cubes.keys())


if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.read().splitlines()
        cubes = { (0, y, x): True for y in range(len(lines)) for x, s in enumerate(lines[y]) if s == '#' }
    print(part1(cubes))  # 295
    print(part2({ (0, *c): True for c in cubes }))  # 1972
