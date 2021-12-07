#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Callable


def _find_min(crabs: list, cost_func: Callable[[int], int]) -> int:
    m, M = min(crabs), max(crabs)
    for x in range(m, M + 1):
        cost = sum(cost_func(abs(c - x)) for c in crabs)
        if 'last' in vars() and last < cost:
            return last
        last = cost


def part1(crabs: list) -> int:
    return _find_min(crabs, lambda x: x)


@lru_cache(maxsize=None)
def _cost2(n: int) -> int:
    return sum(range(1, n + 1))


def part2(crabs: list) -> int:
    return _find_min(crabs, _cost2)


if __name__ == '__main__':
    with open('input.txt') as f:
        crabs = list(map(int, f.read().split(',')))
    print(part1(crabs))  # 349357
    print(part2(crabs))  # 96708205
