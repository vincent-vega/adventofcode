#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import lru_cache


def _strength(bridge: list) -> int:
    return sum(map(sum, bridge))


@lru_cache(maxsize=None)
def _strongest_subchain(components: tuple, port: int) -> int:
    compatibles = { c for c in components if port in c }
    strongest = 0
    for c in compatibles:
        mod = list(components)
        mod.remove(c)
        if 0 in c:
            strongest = max(strongest, sum(c))
        else:
            strongest = max(strongest, sum(c) + _strongest_subchain(tuple(mod), c[0] if c[1] == port else c[1]))
    return strongest


def part1(components: list) -> int:
    strongest = 0
    for c in filter(lambda x: 0 in x and x != (0, 0), components):
        mod = list(components)
        mod.remove(c)
        strongest = max(strongest, sum(c) + _strongest_subchain(tuple(mod), c[0] if c[1] == 0 else c[1]))
    return strongest


@lru_cache(maxsize=None)
def _longest_subchain(components: tuple, port: int) -> list:
    compatibles = { c for c in components if port in c }
    longest = []
    for c in compatibles:
        mod = list(components)
        mod.remove(c)
        if 0 in c:
            s = [ c ]
        else:
            s = [ c ] + _longest_subchain(tuple(mod), c[0] if c[1] == port else c[1])
        if len(longest) < len(s) or len(longest) == len(s) and _strength(longest) < _strength(s):
            longest = s
    return longest


def part2(components: list) -> int:
    longest = []
    for c in filter(lambda x: 0 in x and x != (0, 0), components):
        mod = list(components)
        mod.remove(c)
        s = [ c ] + _longest_subchain(tuple(mod), c[0] if c[1] == 0 else c[1])
        if len(longest) < len(s) or len(longest) == len(s) and _strength(longest) < _strength(s):
            longest = s
    return _strength(longest)


if __name__ == '__main__':
    with open('input.txt') as f:
        components = [ tuple(map(int, l.split('/'))) for l in f.read().splitlines() ]
    print(part1(components))  # 1511
    print(part2(components))  # 1471
