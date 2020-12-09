#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def _valid(preamble: set, tot: int) -> bool:
    for p in preamble:
        if tot - p in preamble:
            return True
    return False


def part1(values: list, preamble_len: int) -> int:
    for i in range(preamble_len, len(values)):
        start, end = i - preamble_len, i + preamble_len + 1
        if not _valid(set(values[start:end]), values[i]):
            return values[i]
    raise Exception('Not found')


def part2(values: list, target: int) -> int:
    for i in range(0, len(values) - 1):
        total = values[i]
        for j in range(i + 2, len(values)):
            total += values[j - 1]
            if total > target:
                break
            elif total == target:
                return min(values[i:j]) + max(values[i:j])
    raise Exception('Not found')


if __name__ == '__main__':
    with open('input.txt') as f:
        values = list(map(int, f.read().splitlines()))
    print(part1(values, 25))  # 542529149
    print(part2(values, 542529149))  # 75678618
