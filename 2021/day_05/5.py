#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter, namedtuple
from typing import List
import re

Line = namedtuple('Line', [ 'x1', 'y1', 'x2', 'y2' ])


def _expand(line: Line) -> set:
    (startX, startY), (endX, endY) = sorted([(line.x1, line.y1), (line.x2, line.y2)])
    if startX == endX:
        return { (startX, startY + d) for d in range(endY - startY + 1) }
    elif startY == endY:
        return { (startX + d, startY) for d in range(endX - startX + 1) }
    slope = 1 if startY < endY else -1
    return { (startX + step, startY + step * slope) for step in range(abs(startY - endY) + 1) }


def part1(lines: List[Line]) -> int:
    c = Counter(coord for l in (l for l in lines if l.x1 == l.x2 or l.y1 == l.y2) for coord in _expand(l))
    return sum(1 for count in c.values() if count > 1)


def part2(lines: List[Line]) -> int:
    c = Counter(coord for l in lines for coord in _expand(l))
    return sum(1 for count in c.values() if count > 1)


if __name__ == '__main__':
    with open('input.txt') as f:
        lines = [ Line(*map(int, re.findall(r'-?\d+', line))) for line in f.read().splitlines() ]
    print(part1(lines))  # 5576
    print(part2(lines))  # 18144
