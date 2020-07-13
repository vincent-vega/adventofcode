#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def part1(signal: str) -> str:
    for n in range(100):
        signal = _calc_phase(signal)
    return signal[:8]


def _calc_phase(signal: str) -> str:
    result = ''
    size = len(signal)
    for pos in range(1, size + 1):
        pattern = _pattern(pos, size)
        result += str(sum([ int(signal[i]) * int(pattern[i]) for i in range(size) ]))[-1]
    return result


def _pattern(position: int, size: int) -> str:
    base_pattern = [0, 1, 0, -1]
    pattern = []
    for p in base_pattern:
        pattern.extend([ p ] * position)
    while len(pattern) < size + 1:
        pattern.extend(pattern)
    return pattern[1:size + 1]


def part2(values):
    pass


if __name__ == '__main__':
    with open('input.txt') as f:
        signal = f.read().strip()
    print(part1(signal))  # 45834272
    print(part2(signal))  #
