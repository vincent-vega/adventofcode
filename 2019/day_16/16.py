#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def part1(signal: list) -> str:
    return ''.join(map(str, _run(signal, 100)[:8]))


def part2(signal: list) -> str:
    pass


def _run(signal: list, iterations: int) -> list:
    for _ in range(iterations):
        signal = _fft(signal)
    return signal


def _fft(signal: list) -> str:
    signal_len = len(signal)
    return [ abs(sum([ s * p for (s, p) in zip(signal, _pattern(pos, signal_len)) ])) % 10 for pos in range(1, signal_len + 1) ]


def _pattern(position: int, size: int) -> int:
    base_pattern = [0, 1, 0, -1]
    idx = 0
    count = position
    for _ in range(size):
        count -= 1
        if count == 0:
            count = position
            idx = (idx + 1) % 4
        yield base_pattern[idx]


if __name__ == '__main__':
    with open('input.txt') as f:
        signal = list(map(int, f.read().strip()))
    print(part1(signal))  # 45834272
    print(part2(signal * 10**5))  #
