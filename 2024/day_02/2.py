#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def _is_safe(a: int, b: int, asc: bool) -> bool:
    return (a < b if asc else b < a) and 0 < abs(a - b) < 4


def _is_safe_report(levels: list[int]) -> bool:
    asc = True
    for i in filter(lambda i: levels[i] != levels[i - 1], range(1, len(levels))):
        asc = levels[i] > levels[i - 1]
        break
    return all(_is_safe(levels[i - 1], levels[i], asc) for i in range(1, len(levels)))


def part1(reports: list[list[int]]) -> int:
    return len(list(filter(lambda r: _is_safe_report(r), reports)))


def part2(reports: list[list[int]]) -> int:
    count = 0
    for r in reports:
        if _is_safe_report(r):
            count += 1
            continue
        for i in range(len(r)):
            if _is_safe_report(r[:i] + r[i + 1:]):
                count += 1
                break
    return count


if __name__ == '__main__':
    with open('input.txt') as f:
        reports = [ list(map(int, line.split())) for line in f.read().splitlines() ]
    print(part1(reports))  # 230
    print(part2(reports))  # 301
