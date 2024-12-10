#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict

ROCKS = [
    { 2, 3, 4, 5 },  # -
    { 3, 2 + 1j, 3 + 1j, 4 + 1j, 3 + 2j },  # +
    { 2, 3, 4, 4 + 1j, 4 + 2j },  # L
    { 2, 2 + 1j, 2 + 2j, 2 + 3j },  # |
    { 2, 3, 2 + 1j, 3 + 1j }  # O
]


def _rest(chamber: set[complex], rock: set[complex]) -> bool:
    if any(r.imag == 1 for r in rock):
        return True
    for r in rock:
        if r - 1j in chamber:
            return True
    return False


def _has_room(cache: dict[float, set[float]], rock: set[complex], jet: int) -> bool:
    if jet > 0:  # push right
        if any(r.real > 5 for r in rock):
            return False
        same_height = [ (c, r) for r in rock for c in cache[r.imag] if c > r.real ]
        return len(same_height) == 0 or all(r.real + 1 < c for c, r in same_height)
    else:  # push left
        if any(r.real < 1 for r in rock):
            return False
        same_height = [ (c, r) for r in rock for c in cache[r.imag] if c < r.real ]
        return len(same_height) == 0 or all(r.real - 1 > c for c, r in same_height)


def _fall(rock: set[complex]) -> set:
    return { r - 1j for r in rock }


def _print(chamber: set[complex], rock: set[complex]) -> int:
    system = chamber | rock
    M = int(max(system, key=lambda c: c.imag).imag)
    print('\n')
    for y in range(M, 0, -1):
        print(f'|{"".join([ "#" if x + 1j * y in system else "." for x in range(0, 7)])}|')
    print('+-------+')


def _run(jets: list[int], spawn: int) -> int:
    chamber = set()
    top = 0
    rock_idx = 0
    jet_idx = 0
    cache = defaultdict(set)
    for _ in range(spawn):
        rock = { r + 1j * top + 4j for r in ROCKS[rock_idx] }
        rock_idx = (rock_idx + 1) % len(ROCKS)
        while True:
            j = jets[jet_idx]
            jet_idx = (jet_idx + 1) % len(jets)
            if _has_room(cache, rock, j):
                rock = { r + j for r in rock }
            if _rest(chamber, rock):
                top = max(top, max(map(lambda r: r.imag, rock)))
                chamber |= rock
                for r in rock:
                    cache[r.imag].add(r.real)
                break
            rock = _fall(rock)
    return int(top)


def part1(jets: list[int]) -> int:
    return _run(jets, 2022)


def part2(jets: list[int]) -> int:
    return _run(jets, 1_000_000_000_000)


if __name__ == '__main__':
    with open('input.txt') as f:
        jets = [ 1 if j == '>' else -1 for j in f.read().strip() ]
    # print(part1(jets))  # 3090
    assert part1(jets) == 3090
    # print(part2(jets))  #
