#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def part1(signal: str) -> int:
    for idx in range(len(signal) - 4):
        if len(set(signal[idx:idx + 4])) == 4:
            return idx + 4


def part2(signal: str) -> int:
    for idx in range(len(signal) - 14):
        if len(set(signal[idx:idx + 14])) == 14:
            return idx + 14


if __name__ == '__main__':
    with open('input.txt') as f:
        signal = f.readline()
    print(part1(signal))  # 1480
    print(part2(signal))  # 2746
