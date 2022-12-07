#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from copy import deepcopy
import re


def part1(crates: list[list[str]], procedure: list[list[int]]) -> str:
    for n, c1, c2 in procedure:
        crates[c2 - 1].extend(crates[c1 - 1].pop() for _ in range(n))
    return ''.join(c[-1] for c in crates if c)


def part2(crates: list[list[str]], procedure: list[list[int]]) -> str:
    for n, c1, c2 in procedure:
        crates[c1 - 1], moved = crates[c1 - 1][:-1 * n], crates[c1 - 1][-1 * n:]
        crates[c2 - 1].extend(moved)
    return ''.join(c[-1] for c in crates if c)


if __name__ == '__main__':
    with open('input.txt') as f:
        status, procedure = [ chunk.split('\n') for chunk in f.read().split('\n\n') ]
        procedure = list(map(lambda p: list(map(int, re.findall(r'\d+', p))), procedure[:-1]))
        size = int(status[-1].strip()[-1])
        crates = [ [] for _ in range(size) ]
        for s in status[:-1]:
            for n, i in filter(lambda x: s[x[1]] != ' ', enumerate(range(1, 4 * size, 4))):
                crates[n].insert(0, s[i])
    print(part1(deepcopy(crates), procedure))  # PTWLTDSJV
    print(part2(crates, procedure))  # WZMFVGGZP
