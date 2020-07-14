#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def part1(signal: list) -> str:
    patterns = [ _pattern(pos, len(signal)) for pos in range(1, len(signal) + 1) ]
    for n in range(100):
        signal = _fft(signal, patterns)
    return ''.join(map(str, signal[:8]))


def _fft(signal: list, patterns: list) -> str:
    return [ abs(sum([ s * p for (s, p) in zip(signal, pattern) ])) % 10 for pattern in patterns ]


def _pattern(position: int, size: int) -> list:
    base_pattern = [0, 1, 0, -1]
    pattern = []
    for p in base_pattern:
        pattern.extend([ p ] * position)
    while len(pattern) < size + 1:
        pattern.extend(pattern)
    return pattern[1:size + 1]


def part2(signal: list):
    pass


if __name__ == '__main__':
    with open('input.txt') as f:
        signal = list(map(int, f.read().strip()))
    print(part1(signal))  # 45834272
    print(part2(signal * 10**5))  #
