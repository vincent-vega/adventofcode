#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce
import re


def part1(time: tuple[int], distance: tuple[int]) -> int:
    return reduce(lambda a, b: a * b, [ sum([ 1 for tt in range(1, t + 1) if tt * (t - tt) > d ]) for t, d in zip(time, distance) ])


def part2(time: tuple[int], distance: tuple[int]) -> int:
    time = int(''.join(map(str, time)))
    distance = int(''.join(map(str, distance)))
    return sum([ 1 for t in range(1, time + 1) if t * (time - t) > distance ])


if __name__ == '__main__':
    with open('input.txt') as f:
        time, distance = [ tuple(map(int, re.findall(r'\d+', line.split(':')[1]))) for line in f.read().splitlines() ]
    print(part1(time, distance))  # 771628
    print(part2(time, distance))  # 27363861
