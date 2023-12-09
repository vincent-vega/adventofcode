#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re


def _nxt(values: tuple[int]) -> tuple[int]:
    return tuple(values[i + 1] - values[i] for i in range(len(values) - 1))


def _seq(values: tuple[int], first: bool = False) -> tuple[int]:
    sequence = [ tuple(values) ]
    while True:
        nxt = _nxt(values)
        for n in (x for x in nxt if x != 0):
            break
        else:
            break
        sequence.append(nxt)
        values = nxt
    return tuple(s[0] if first else s[-1] for s in sequence)


def _predict1(sequence: tuple[int], diff: int = 0) -> int:
    for i in range(len(sequence) - 1, -1, -1):
        diff += sequence[i]
    return diff


def part1(history: tuple[tuple[int]]) -> int:
    return sum(_predict1(_seq(h)) for h in history)


def _predict2(sequence: tuple[int], diff: int = 0) -> int:
    for i in range(len(sequence) - 1, -1, -1):
        diff = sequence[i] - diff
    return diff


def part2(history: tuple[tuple[int]]) -> int:
    return sum(_predict2(_seq(h, True)) for h in history)


if __name__ == '__main__':
    with open('input.txt') as f:
        history = tuple(tuple(map(int, re.findall(r'-?\d+', line))) for line in f.read().splitlines())
    print(part1(history))  # 1955513104
    print(part2(history))  # 1131
