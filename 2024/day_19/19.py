#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import cache


def part1(patterns: set[str], designs: list[str]) -> int:
    s = min(map(len, patterns))
    S = max(map(len, patterns))

    @cache
    def _match(design: str) -> int:
        if design in patterns:
            return True
        for n in range(s, min(S, len(design)) + 1):
            if design[:n] in patterns and _match(design[n:]):
                return True
        return False

    return sum(_match(d) for d in designs)


def part2(patterns: set[str], designs: list[str]) -> int:
    s = min(map(len, patterns))
    S = max(map(len, patterns))

    @cache
    def _match(design: str) -> int:
        count = 0
        for n in range(s, min(S, len(design)) + 1):
            if design[:n] in patterns:
                count += 1 if len(design) == n else _match(design[n:])
        return count

    return sum(_match(d) for d in designs)


if __name__ == '__main__':
    with open('input.txt') as f:
        patterns, designs = f.read().split('\n\n')
        patterns = set(patterns.split(', '))
        designs = designs.split()
    print(part1(patterns, designs))  # 330
    print(part2(patterns, designs))  # 950763269786650
