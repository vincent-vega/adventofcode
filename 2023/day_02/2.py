#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from functools import reduce


def _check_grab(g: str, cubes: dict) -> bool:
    n, c = g.split(' ')
    return c in cubes and int(n) <= cubes[c]


def _check_game(game: list[str], cubes: dict) -> bool:
    return all(_check_grab(gg, cubes) for g in game for gg in g.split(', '))


def part1(games: list[list[str]]) -> int:
    cubes = { 'red': 12, 'green': 13, 'blue': 14 }
    return sum(n for n, g in enumerate(games, 1) if _check_game(g, cubes))


def _power(game: list[str]) -> int:
    s = defaultdict(int)
    for grab in game:
        grab = grab.split(', ')
        for g in grab:
            n, c = g.split(' ')
            s[c] = max(int(n), s[c])
    return reduce(lambda a, b: a * b, s.values())


def part2(games: list[list[str]]) -> int:
    return sum(_power(g) for g in games)


if __name__ == '__main__':
    with open('input.txt') as f:
        games = [ line[line.index(":") + 2:].split('; ') for line in f.read().splitlines() ]
    print(part1(games))  # 2204
    print(part2(games))  # 71036
