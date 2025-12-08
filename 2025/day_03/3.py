#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def part1(banks: list[list[int]]) -> int:
    joltage = 0
    for bank in banks:
        *_, m, M = sorted(bank)
        pivot = bank.index(M)
        if pivot != len(bank) - 1:
            joltage += M * 10 + max(bank[pivot + 1:])
            continue
        pivot = bank.index(m)
        joltage += m * 10 + max(bank[pivot + 1:])
    return joltage


def part2(banks: list[list[int]], size: int = 12) -> int:
    joltage = 0
    for bank in banks:
        skip = len(bank) - size
        largest = []
        idx = 0
        while idx < len(bank) and len(largest) < size:
            if skip:
                window = bank[idx:idx + skip + 1]
                m, M = min(window), max(window)
                if m < M and window[0] == m:
                    skip -= 1
                    idx += 1
                    continue
                largest.append(M)
                i = window.index(M)
                skip -= i
                idx += i + 1
                continue
            largest.extend(bank[idx:])
        joltage += sum(10 ** t * n for t, n in enumerate(largest[::-1]))
    return joltage


if __name__ == '__main__':
    with open('input.txt') as f:
        values = [ list(map(int, line)) for line in f.read().splitlines() ]
    assert part1(values) == 17766
    assert part2(values) == 176582889354075
