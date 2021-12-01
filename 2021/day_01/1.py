#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def part1(depths: list) -> int:
    return sum(1 for idx in range(1, len(depths)) if depths[idx] > depths[idx - 1])


def part2(depths: list) -> int:
    return sum(1 for idx in range(3, len(depths)) if depths[idx] > depths[idx - 3])  # skip common values


if __name__ == '__main__':
    with open('input.txt') as f:
        depths = [ int(x) for x in f ]
    print(part1(depths))  # 1553
    print(part2(depths))  # 1597
