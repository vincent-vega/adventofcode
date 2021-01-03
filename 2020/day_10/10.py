#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import lru_cache
from itertools import combinations
import doctest


def _fill_up(values: list) -> list:
    return [ 0 ] + values + [ values[-1] + 3 ]


def _valid(values: list) -> bool:
    for i in range(1, len(values)):
        if values[i] - values[i - 1] > 3:
            return False
    return True


@lru_cache(maxsize=None)
def _gaps(size: int) -> list:
    # check the whole subchain too
    return [ () ] + [ j for i in range(1, size - 1) for j in combinations(range(1, size - 1), i) ]


def _count(subchain: list) -> int:
    """
    Count the number of valid subchains

    >>> _count([0, 3, 4, 5, 8])
    2
    """
    # TODO check around gaps only
    return sum([ 1 if _valid([ v for i, v in enumerate(subchain) if i not in g]) else 0 for g in _gaps(len(subchain)) ])


def part1(values: list) -> int:
    jolt_1, jolt_3 = 0, 0
    values = _fill_up(values)
    for i in range(1, len(values)):
        if values[i] - values[i - 1] == 1:
            jolt_1 += 1
        elif values[i] - values[i - 1] == 3:
            jolt_3 += 1
    return jolt_1 * jolt_3


def part2(values: list) -> int:
    values = _fill_up(values)
    idx, count = 0, 1
    while idx < len(values) - 2:
        if values[idx + 2] - values[idx] <= 3:
            # gap found
            # get the whole subchain (in case the gaps are more than one)
            nxt = 3
            while idx + nxt < len(values) and values[idx + nxt] - values[idx + nxt - 2] <= 3:
                nxt += 1
            count *= _count(values[idx:idx + nxt + 1])
            idx += nxt
        else:
            idx += 1
    return count


if __name__ == '__main__':
    with open('input.txt') as f:
        values = sorted(list(map(int, f.read().splitlines())))
    doctest.testmod()
    print(part1(values))  # 1885
    print(part2(values))  # 2024782584832
