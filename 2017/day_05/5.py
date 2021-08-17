#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Callable


def _run(offsets: list, update_f: Callable) -> int:
    cnt, cur, nxt = 0, 0, 0
    while cur < len(offsets):
        nxt = offsets[cur]
        offsets[cur] += update_f(offsets[cur])
        cur += nxt
        cnt += 1
    return cnt


def part1(offsets: list) -> int:
    return _run(list(offsets), lambda x: 1)


def part2(offsets: list) -> int:
    return _run(list(offsets), lambda x: -1 if x > 2 else 1)


if __name__ == '__main__':
    with open('input.txt') as f:
        offsets = list(map(int, f.read().splitlines()))
    print(part1(offsets))  # 396086
    print(part2(offsets))  # 28675390
