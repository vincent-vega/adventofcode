#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from doctest import testmod
from typing import Generator


def part1(signal: list, phase_num: int) -> str:
    for _ in range(phase_num):
        signal = _fft(signal)
    return ''.join(map(str, signal[:8]))


def part2(signal: list, phase_num: int, offset_size: int) -> str:
    offset = sum([ signal[exp] * 10**(offset_size - exp - 1) for exp in range(offset_size) ])
    assert offset > int(len(signal) / 2)
    signal = signal[offset:]
    for _ in range(phase_num):
        signal_tmp = []
        accumulator = 0
        for idx in range(len(signal) - 1, -1, -1):
            accumulator = (accumulator + signal[idx]) % 10
            signal_tmp.append(accumulator)
        signal = signal_tmp[::-1]
    return ''.join(map(str, signal[:8]))


def _fft(signal: list) -> list:
    return _fft_first(signal) + _fft_second(signal, int(len(signal) / 2))


def _fft_first(signal: list) -> list:
    size = len(signal)
    return [ abs(sum([ s * p for (s, p) in zip(signal, _pattern(pos, size)) ])) % 10 for pos in range(1, int(size / 2) + 1) ]


def _fft_second(signal: list, offset: int=0) -> list:
    """
    >>> a = [ 1 ] * 18
    >>> _fft_second(a, int(len(a) / 2))
    [9, 8, 7, 6, 5, 4, 3, 2, 1]
    >>> a = [ 1 ] * 15
    >>> _fft_second(a, int(len(a) / 2))
    [8, 7, 6, 5, 4, 3, 2, 1]
    >>> a = [ 10 ] * 15
    >>> _fft_second(a, int(len(a) / 2))
    [0, 0, 0, 0, 0, 0, 0, 0]
    """

    return [ sum(signal[idx:]) % 10 for idx in range(offset, len(signal)) ]


def _pattern(position: int, size: int) -> Generator[int, None, None]:
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
    testmod()
    with open('input.txt') as f:
        signal = list(map(int, f.read().strip()))
    print(part1(signal, 100))  # 45834272
    print(part2(signal * 10**4, 100, 7))  # 37615297
