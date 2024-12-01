#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter
import bisect


def part1(left: list, right: list) -> int:
    return sum(abs(a - b) for a, b in zip(left, right))


def part2(left: list, right: list) -> int:
    c = Counter(right)
    return sum(n * c[n] for n in left)


if __name__ == '__main__':
    left = []
    right = []
    with open('input.txt') as a:
        for a, b in (map(int, line.split()) for line in a.read().splitlines()):
            bisect.insort(left, a)
            bisect.insort(right, b)
    print(part1(left, right))  # 2196996
    print(part2(left, right))  # 23655822
