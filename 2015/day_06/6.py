#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import namedtuple
import re

Instruction = namedtuple('Instruction', [ 'action', 'start', 'end' ])


def part1(instructions: list) -> int:
    grid = {}
    for i in instructions:
        start_x, start_y = i.start
        end_x, end_y = i.end
        for y in range(start_y, end_y + 1):
            for x in range(start_x, end_x + 1):
                if i.action == 'on':
                    grid[(x, y)] = True
                elif i.action == 'off':
                    grid[(x, y)] = False
                else:
                    grid[(x, y)] = not grid.get((x, y), False)
    return sum(( 1 for v in grid.values() if v ))


def part2(instructions: list) -> int:
    grid = {}
    for i in instructions:
        start_x, start_y = i.start
        end_x, end_y = i.end
        for y in range(start_y, end_y + 1):
            for x in range(start_x, end_x + 1):
                if i.action == 'on':
                    grid[(x, y)] = grid.get((x, y), 0) + 1
                elif i.action == 'off':
                    grid[(x, y)] = max(0, grid.get((x, y), 0) - 1)
                else:
                    grid[(x, y)] = grid.get((x, y), 0) + 2
    return sum(grid.values())


def _parse(line: str) -> Instruction:
    start, end = re.findall(r'\d+,\d+', line)
    line = line.split()
    action = 'on' if line[1] == 'on' else 'off' if line[1] == 'off' else 'toggle'
    return Instruction(action, tuple(map(int, start.split(','))), tuple(map(int, end.split(','))))


if __name__ == '__main__':
    with open('input.txt') as f:
        instructions = list(map(_parse, f.read().splitlines()))
    print(part1(instructions))  # 543903
    print(part2(instructions))  # 14687245
