#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def part1(values: list) -> int:
    return sum([ max(row) - min(row) for row in values ])


def _chk(row: list) -> int:
    for i in range(len(row)):
        for j in range(i + 1, len(row)):
            if row[i] % row[j] == 0:
                return row[i] // row[j]
            if row[j] % row[i] == 0:
                return row[j] // row[i]
    raise Exception('Not found')


def part2(values: list) -> int:
    return sum(map(_chk, values))


if __name__ == '__main__':
    with open('input.txt') as f:
        values = [ list(map(int, r.split('\t'))) for r in f.read().splitlines() ]
    print(part1(values))  # 21845
    print(part2(values))  # 191
