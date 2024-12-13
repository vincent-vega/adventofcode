#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re


def _tokens(x1: int, y1: int, x2: int, y2: int, x: int, y: int, addend: int = 0) -> int:
    '''
    This function computes the machines of n1 and n2 using formulas derived from
    solving the linear system
    '''
    n2 = (y1 * (x + addend) - x1 * (y + addend)) / (y1 * x2 - x1 * y2)
    n1 = ((x + addend) - x2 * n2) / x1
    return 3 * n1 + n2 if all(n % 1 == 0 for n in (n1, n2)) else 0


def part1(machines: tuple[int]) -> int:
    return int(sum(_tokens(*m) for m in machines))


def part2(machines: tuple[int]) -> int:
    return int(sum(_tokens(*m, 10000000000000) for m in machines))


if __name__ == '__main__':
    with open('input.txt') as f:
        machines = [ tuple(map(int, re.findall(r'\d+', block))) for block in f.read().split('\n\n') ]
    print(part1(machines))  # 36571
    print(part2(machines))  # 85527711500010
