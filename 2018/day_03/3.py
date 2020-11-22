#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
import re


def part1(values: list) -> int:
    area = [ [ 0 for x in range(1000) ] for y in range(1000) ]
    count = 0
    for claim in values:
        coord = re.search('^.+\s([0-9]+,[0-9]+):.+$', claim).group(1)
        y, x = [ int(n) for n in coord.split(',') ]
        size = re.search('^.+:\s([0-9]+x[0-9]+)$', claim).group(1)
        dim_y, dim_x = [ int(n) for n in size.split('x') ]
        for r in range(x, x + dim_x):
            for c in range(y, y + dim_y):
                if area[r][c] == 1:
                    area[r][c] += 1
                    count += 1
                elif area[r][c] == 0:
                    area[r][c] += 1
    return count


def part2(values: list) -> int:
    def extract(s):
        return [ int(x) for x in re.findall(r'-?\d+', s) ]
    area = defaultdict(int)
    double = defaultdict(bool)
    data = [ extract(claim) for claim in values ]
    for n, x, y, l, w in data:
        for i in range(l):
            for j in range(w):
                offset = i + x, j + y
                if area[offset] == 0:
                    area[offset] = n
                else:
                    double[n] = double[area[offset]] = True
    return [ x for x in range(1, len(data) + 1) if x not in double.keys() ][0]


if __name__ == '__main__':
    with open('input.txt') as f:
        values = f.read().splitlines()
    print(part1(values))  # 119551
    print(part2(values))  # 1124
