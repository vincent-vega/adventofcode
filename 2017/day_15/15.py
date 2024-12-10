#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Generator


def _lowest16(n: int) -> int:
    return n & 65535


def _nxt(start: tuple[int, int], factor: tuple[int, int], cnt: int) -> Generator[tuple, None, None]:
    curA, curB = start
    factorA, factorB = factor
    for _ in range(cnt):
        curA = (curA * factorA) % 2147483647
        curB = (curB * factorB) % 2147483647
        yield curA, curB


def _nxt2(start: tuple[int, int], factor: tuple[int, int], cnt: int) -> Generator[tuple, None, None]:
    curA, curB = start
    factorA, factorB = factor
    for _ in range(cnt):
        while True:
            curA = (curA * factorA) % 2147483647
            if curA % 4 == 0:
                break
        while True:
            curB = (curB * factorB) % 2147483647
            if curB % 8 == 0:
                break
        yield curA, curB


def part1(genA: tuple[int, int], genB: tuple[int, int], cnt: int) -> int:
    startA, factorA = genA
    startB, factorB = genB
    return sum([ 1 for a, b in _nxt((startA, startB), (factorA, factorB), cnt) if _lowest16(a) == _lowest16(b) ])


def part2(genA: tuple[int, int], genB: tuple[int, int], cnt: int) -> int:
    startA, factorA = genA
    startB, factorB = genB
    return sum([ 1 for a, b in _nxt2((startA, startB), (factorA, factorB), cnt) if _lowest16(a) == _lowest16(b) ])


if __name__ == '__main__':
    with open('input.txt') as f:
        startA, startB = [ int(line.split()[-1]) for line in f.read().splitlines() ]
    print(part1((startA, 16807), (startB, 48271), 40_000_000))  # 577
    print(part2((startA, 16807), (startB, 48271), 5_000_000))  # 316
