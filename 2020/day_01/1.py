#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import combinations


def part1(values: list, tot: int) -> int:
    for v1, v2 in combinations(values, 2):
        if v1 + v2 == tot:
            return v1 * v2


def part2(values: list, tot: int) -> int:
    for v1, v2, v3 in combinations(values, 3):
        if v1 + v2 + v3 == tot:
            return v1 * v2 * v3


if __name__ == '__main__':
    with open('input.txt') as f:
        values = [ int(x) for x in f ]
    print(part1(values, 2020))  # 805731
    print(part2(values, 2020))  # 192684960
