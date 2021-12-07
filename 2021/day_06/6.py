#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import lru_cache


def part1(ages: list, days: int) -> int:
    for _ in range(days):
        nxt = []
        children = 0
        for n in ages:
            if n == 0:
                children += 1
            nxt.append(6 if n == 0 else n - 1)
        ages = nxt + [8] * children
    return len(ages)


@lru_cache(maxsize=None)
def _children(offset: int, days: int) -> int:
    mine = max(0, days - offset - 2) // 7
    return mine + sum(_children(n, days) for n in range(offset + 9, days + 1, 7))


def part2(ages: list, days: int) -> int:
    cnt = len(ages)
    for offset in ages:
        mine = (1 if days > offset else 0) + max(0, days - offset - 1) // 7
        others = sum(_children(o, days) for o in range(offset + 1, days + 1, 7))
        cnt += mine + others
    return cnt


if __name__ == '__main__':
    with open('input.txt') as f:
        ages = list(map(int, f.read().split(',')))
    print(part1(ages, 80))  # 360610
    print(part2(ages, 256))  # 1631629590423
