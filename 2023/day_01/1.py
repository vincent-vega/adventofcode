#!/usr/bin/env python3
# -*- coding: utf-8 -*-

NUMBERS = [ 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine' ]


def _filter(s: list[int]) -> int:
    return 10 * s[0] + s[-1]


def _transform(s: str) -> list[int]:
    return [ int(c) for c in s if c.isdigit() ]


def part1(lines: list[str]) -> int:
    return sum(_filter(_transform(line)) for line in lines)


def _find(line: str, last=False) -> int:
    if last:
        line = line[::-1]
    for n, c in enumerate(line):
        if c.isdigit():
            return int(c)
        for v, num in enumerate(NUMBERS, 1):
            if last:
                num = num[::-1]
            if len(line) - n >= len(num) and line[n:n + len(num)] == num:
                return v


def part2(lines: list[str]) -> int:
    return sum(10 * _find(line) + _find(line, True) for line in lines)


if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.read().splitlines()
    print(part1(lines))  # 53386
    print(part2(lines))  # 53312
