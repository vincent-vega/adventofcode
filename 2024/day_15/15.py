#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.lib import _print


def _nxt(x, y, d):
    if d == '^':
        return x, y - 1
    elif d == '>':
        return x + 1, y
    elif d == 'v':
        return x, y + 1
    elif d == '<':
        return x - 1, y


def part1(robot, walls, boxes, moves):
    for m in moves:
        c = _nxt(*robot, m)
        boxes_to_move = set()
        while c in boxes:
            boxes_to_move.add(c)
            c = _nxt(*c, m)
        if c in walls:
            continue
        if boxes_to_move:
            boxes = { _nxt(x, y, m) if (x, y) in boxes_to_move else (x, y) for x, y in boxes }
        robot = _nxt(*robot, m)
    return sum(x + 100 * y for x, y in boxes)


def part2(values):
    pass


# import pudb; pu.db
if __name__ == '__main__':
    # with open('example1.txt') as f:
    with open('input.txt') as f:
        warehouse, moves = f.read().split('\n\n')
        walls = set()
        boxes = set()
        for y, line in enumerate(warehouse.split()):
            for x, c in enumerate(line):
                if c == '@':
                    robot = (x, y)
                elif c == '#':
                    walls.add((x, y))
                elif c == 'O':
                    boxes.add((x, y))
        moves = ''.join(map(str.strip, moves))
    _print(part1(robot, walls, boxes, moves))  # 1526018
    # _print(part2(values))  #
