#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import namedtuple
import re

Claim = namedtuple('Claim', [ 'id', 'offset_x', 'offset_y', 'width', 'height' ])


def part1(claims: tuple) -> int:
    area = tuple([ 0 for x in range(1000) ] for y in range(1000))
    count = 0
    for c in claims:
        for x in range(c.offset_x, c.offset_x + c.width):
            for y in range(c.offset_y, c.offset_y + c.height):
                if area[x][y] == 1:
                    area[x][y] += 1
                    count += 1
                elif area[x][y] == 0:
                    area[x][y] += 1
    return count


def part2(claims: tuple) -> int:
    area = {}
    double = set()
    for c in claims:
        for i in range(c.width):
            for j in range(c.height):
                offset = i + c.offset_x, j + c.offset_y
                if area.get(offset, 0) == 0:
                    area[offset] = c.id
                else:
                    double.update([ c.id, area.get(offset, 0) ])
    return min(set(range(1, len(claims) + 1)) - double)


if __name__ == '__main__':
    with open('input.txt') as f:
        claims = tuple(Claim(*list(map(int, re.findall(r'\d+', line)))) for line in f.read().splitlines())
    print(part1(claims))  # 119551
    print(part2(claims))  # 1124
