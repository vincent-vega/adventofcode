#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re


def part1(values: list) -> int:
    area = [ [ 0 for x in range(1000) ] for y in range(1000) ]
    count = 0
    for claim in values:
        y, x = map(int, re.search(r'^.+\s(\d+,\d+):.+$', claim).group(1).split(','))
        dim_y, dim_x = map(int, re.search(r'^.+:\s(\d+x\d+)$', claim).group(1).split('x'))
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
        return tuple(int(x) for x in re.findall(r'-?\d+', s))
    area = {}
    double = set()
    data = [ extract(claim) for claim in values ]
    for n, x, y, l, w in data:
        for i in range(l):
            for j in range(w):
                offset = i + x, j + y
                if area.get(offset, 0) == 0:
                    area[offset] = n
                else:
                    double.update([ n, area.get(offset, 0) ])
    return min(set(range(1, len(data) + 1)) - double)


if __name__ == '__main__':
    with open('input.txt') as f:
        values = f.read().splitlines()
    print(part1(values))  # 119551
    print(part2(values))  # 1124
