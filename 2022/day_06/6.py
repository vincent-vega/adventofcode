#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def _detect(signal: str, n: int) -> int:
    for idx in range(4, len(signal)):
        if len(set(signal[idx - n:idx])) == n:
            return idx


def part1(signal: str) -> int:
    return _detect(signal, 4)


def part2(signal: str) -> int:
    return _detect(signal, 14)


if __name__ == '__main__':
    with open('input.txt') as f:
        signal = f.readline()
    print(part1(signal))  # 1480
    print(part2(signal))  # 2746
