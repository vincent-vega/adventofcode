#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def _captcha(values: list, offset: int) -> int:
    return sum(values[i] for i in range(len(values)) if values[i] == values[(i + offset) % len(values)])


def part1(values: list) -> int:
    return _captcha(values, 1)


def part2(values: list) -> int:
    return _captcha(values, len(values) // 2)


if __name__ == '__main__':
    with open('input.txt') as f:
        values = [ list(map(int, l)) for l in f.read().splitlines() ]
    print(*[ part1(v) for v in values ], sep='\n')  # 1203
    print(*[ part2(v) for v in values ], sep='\n')  # 1146
