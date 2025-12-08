#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.lib import fulladj


def part1(rolls: set[tuple[int, int]]) -> int:
    return sum(1 for r in rolls if sum(1 for a in fulladj(*r) if a in rolls) < 4)


def part2(rolls: set[tuple[int, int]]) -> int:
    count = 0
    while removed := { r for r in rolls if sum(1 for a in fulladj(*r) if a in rolls) < 4 }:
        count += len(removed)
        rolls -= removed
    return count


if __name__ == '__main__':
    with open('input.txt') as f:
        rolls = { (x, y) for y, line in enumerate(f.read().splitlines()) for x, c in enumerate(line) if c == '@'}
    print(part1(rolls))  # 1397
    print(part2(rolls))  # 8758
