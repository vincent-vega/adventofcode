#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque


def _whirl(steps: int, cnt: int, target: int) -> int:
    buf = deque([ 0 ])
    steps *= -1
    for n in range(1, cnt + 1):
        buf.rotate(steps)
        buf.append(n)
    return buf[(buf.index(target) + 1) % len(buf)]


def part1(steps: int, cnt: int) -> int:
    return _whirl(steps, cnt, 2017)


def part2(steps: int, cnt: int) -> int:
    result = None
    cur = 0
    for n in range(1, cnt + 1):
        cur = (cur + steps) % n + 1
        if cur == 1:
            result = n
    return result


if __name__ == '__main__':
    print(part1(324, 2017))  # 1306
    print(part2(324, 50_000_000))  # 20430489
