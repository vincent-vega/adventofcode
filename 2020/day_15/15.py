#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def _play(values: list, rounds: int) -> int:
    old, new = {}, { v: i + 1 for i, v in enumerate(values) }
    last = values[-1]
    for r in range(len(values) + 1, rounds + 1):
        if last in old.keys():
            last = new[last] - old[last]
        else:
            last = 0
        if last in new.keys():
            old[last] = new[last]
        new[last] = r
    return last


def part1(values: list) -> int:
    return _play(values, 2020)


def part2(values: list) -> int:
    return _play(values, 30000000)


if __name__ == "__main__":
    with open('input.txt') as f:
        values = list(map(int, f.readline().split(',')))
    print(part1(values))  # 403
    print(part2(values))  # 6823
