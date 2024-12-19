#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import cache


def part1(towels: set[str], designs: list[str]) -> int:
    s = min(map(len, towels))
    S = max(map(len, towels))

    @cache
    def _match(design: str, s: int, S: int) -> int:
        if design in towels:
            return True
        for n in range(s, min(S, len(design)) + 1):
            if design[:n] in towels and _match(design[n:], s, S):
                return True
        return False

    return sum(_match(d, s, S) for d in designs)


def part2(towels: set[str], designs: list[str]) -> int:
    s = min(map(len, towels))
    S = max(map(len, towels))

    @cache
    def _match(design: str, s: int, S: int) -> int:
        count = 0
        for n in range(s, min(S, len(design)) + 1):
            if design[:n] in towels:
                if len(design) - n == 0:
                    count += 1
                elif (c := _match(design[n:], s, S)) > 0:
                    count += c
        return count

    return sum(_match(d, s, S) for d in designs)


if __name__ == '__main__':
    with open('input.txt') as f:
        towels, designs = f.read().split('\n\n')
        towels = set(towels.split(', '))
        designs = designs.split()
    print(part1(towels, designs))  # 330
    print(part2(towels, designs))  # 950763269786650
