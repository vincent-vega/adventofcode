#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass


def _nxt(x, y, d):
    if d == '^':
        return x, y - 1
    elif d == '>':
        return x + 1, y
    elif d == 'v':
        return x, y + 1
    elif d == '<':
        return x - 1, y


def part1(robot: tuple[int], walls: set[tuple[int]], boxes: set[tuple[int]], moves: str) -> int:
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


@dataclass
class Box:
    coord: tuple[tuple[int]]


def part2(robot: tuple[int], walls: set[tuple[int]], boxes: set[tuple[int]], moves: str) -> int:
    robot = (2 * robot[0], robot[1])
    walls = { (2 * x + dx, y) for x, y in walls for dx in (0, 1) }
    boxes = [ Box(((2 * x, y), (2 * x + 1, y))) for x, y in boxes ]
    boxes_coord = { c for b in boxes for c in b.coord }
    for move in moves:
        x, y = robot
        nxt = _nxt(x, y, move)
        if move in '<>' and nxt in boxes_coord:
            boxes_to_move = 1
            xx, _ = nxt
            dx = 1 if move == '>' else -1
            while (xx + 2 * dx, y) in boxes_coord:
                boxes_to_move += 1
                xx += 2 * dx
            if (xx + 2 * dx, y) in walls:
                continue
            if coord_to_be_moved := { (x + n * dx * 2 + nn, y) for n in range(1, boxes_to_move + 1) for nn in (0, 1) }:
                for box in boxes:
                    b1, b2 = box.coord
                    if b1 in coord_to_be_moved or b2 in coord_to_be_moved:
                        box.coord = (_nxt(*b1, move), _nxt(*b2, move))
                boxes_coord = { c for b in boxes for c in b.coord }
            robot = nxt
        elif move in '<>' and nxt not in walls:
            robot = nxt
        elif move in '^v' and nxt in boxes_coord:
            dy = 1 if move == 'v' else -1
            boxes_to_move = []
            coord_to_check = set([ nxt ])
            changed = True
            cannot_move = False
            while changed:
                changed = False
                if any(c in walls for c in coord_to_check):
                    cannot_move = True
                    break
                for box in boxes:
                    (x1, y1), (x2, y2) = box.coord
                    if ((x1, y1) in coord_to_check or (x2, y2) in coord_to_check) and box not in boxes_to_move:  # TODO fixme
                        boxes_to_move.append(box)
                        coord_to_check -= { (x1, y1), (x2, y2) }
                        coord_to_check |= { (x1, y1 + 1 * dy), (x2, y2 + 1 * dy) }
                        changed = True
            if cannot_move:
                continue
            if boxes_to_move:
                for box in boxes_to_move:
                    b1, b2 = box.coord
                    box.coord = (_nxt(*b1, move), _nxt(*b2, move))
                boxes_coord = { c for b in boxes for c in b.coord }
            robot = nxt
        elif move in '^v' and nxt not in walls:
            robot = nxt
    return sum(x + 100 * y for x, y in map(lambda b: b.coord[0], boxes))


if __name__ == '__main__':
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
    print(part1(robot, walls, boxes, moves))  # 1526018
    print(part2(robot, walls, boxes, moves))  # 1550677
