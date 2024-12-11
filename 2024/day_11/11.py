#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter, defaultdict
import math
import re


def _conv(n: int) -> list[int] | tuple[int]:
    if n == 0:
        return [ 1 ]
    elif (digits := math.floor(math.log(n, 10)) + 1) % 2 == 0:
        return divmod(n, 10 ** (digits // 2))
    else:
        return [ n * 2024 ]


def _blink1(stones: list[int]) -> list[int]:
    return [ k for n in stones for k in _conv(n) ]


def part1(stones: list[int]) -> int:
    for _ in range(25):
        stones = _blink1(stones)
    return len(stones)


def _blink2(stones: dict[int, int]) -> dict[int, int]:
    nxt = defaultdict(int)
    for n, count in stones.items():
        for k in _conv(n):
            nxt[k] += count
    return nxt


def part2(stones: list[int]) -> int:
    stones = Counter(stones)
    for _ in range(75):
        stones = _blink2(stones)
    return sum(stones.values())


if __name__ == '__main__':
    with open('input.txt') as f:
        stones = list(map(int, re.findall(r'\d+', f.read())))
    print(part1(stones))  # 197357
    print(part2(stones))  # 234568186890978
