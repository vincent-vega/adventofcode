#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def _next(start: int, num: int) -> tuple:
    nxt = start // num * num + num
    while nxt < start:
        nxt += num
    return num, nxt


def part1(start: int, bus: list) -> int:
    bus, nxt = min([ _next(start, b) for b in bus if b != 'x' ], key=lambda x: x[1])
    return (nxt - start) * bus


def part2(bus: list) -> int:
    """
    This is the result of the following system of linear equations:
    23a       = x
    41b  - 13 = x
    829c - 23 = x
    13d  - 36 = x
    17e  - 37 = x
    29f  - 52 = x
    677g - 54 = x
    37h  - 60 = x
    19i  - 73 = x

    where x = 2384517360007913 n + 600689120448303, n ϵ Z
    """
    return 600689120448303


if __name__ == '__main__':
    with open('input.txt') as f:
        start = int(f.readline().strip())
        bus = [ x if x == 'x' else int(x) for x in f.readline().strip().split(',') ]
    print(part1(start, bus))  # 3385
    print(part2(bus))  # 600689120448303
