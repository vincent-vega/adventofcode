#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def part1(values: list) -> int:
    return sum(values)


def part2(values: list) -> int:
    freq = set()
    current = 0
    while True:
        for v in values:
            current += v
            if current in freq:
                return current
            freq.add(current)


if __name__ == '__main__':
    with open('input.txt') as f:
        values = list(map(int, f.read().splitlines()))
    print(part1(values))  # 493
    print(part2(values))  # 413
