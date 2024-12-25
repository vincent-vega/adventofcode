#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def _fit(key: list[int], lock: list[int]) -> bool:
    return all(key[n] + lock[n] < 6 for n in range(5))


def part1(keys: list[list[int]], locks: list[list[int]]) -> int:
    return sum(_fit(a, b) for a in keys for b in locks)


if __name__ == '__main__':
    with open('input.txt') as f:
        locks = []
        keys = []
        for item in f.read().split('\n\n'):
            lines = item.split()
            heights = [ sum(1 for y in range(7) if lines[y][x] == '#') - 1 for x in range(5) ]
            if lines[0] == '#' * 5:
                locks.append(heights)
            else:
                keys.append(heights)
    print(part1(keys, locks))  # 3284
