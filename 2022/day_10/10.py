#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def part1(instructions: list[int]) -> int:
    X = 1
    strenght = cycle = 0
    for n in instructions:
        cycle += 1
        if (cycle - 20) % 40 == 0:
            strenght += cycle * X
        if n is not None:
            cycle += 1
            if (cycle - 20) % 40 == 0:
                strenght += cycle * X
            X += n
    return strenght


def _move(cur: (int, int)) -> (int, int):
    cur_x, cur_y = cur
    cur_x = (cur_x + 1) % 40
    return cur_x, (cur_y + 1) % 6 if cur_x == 0 else cur_y


def _update(screen: set[int, int], cur: (int, int), X: int):
    x, y = cur
    if x in { X - 1, X, X + 1}:
        screen.add((x, y))


def part2(instructions: list[int]) -> str:
    X = 1
    cycle = 0
    cur = (0, 0)
    screen = set()
    for n in instructions:
        cycle += 1
        _update(screen, cur, X)
        cur = _move(cur)
        if n is not None:
            cycle += 1
            _update(screen, cur, X)
            cur = _move(cur)
            X += n
    return '\n'.join([ ''.join([ '#' if (x, y) in screen else ' ' for x in range(40) ]) for y in range(6) ])


if __name__ == '__main__':
    with open('input.txt') as f:
        instructions = [ None if line == 'noop' else int(line.split()[1]) for line in f.read().splitlines() ]
    print(part1(instructions))  # 13480
    print(part2(instructions))  # EGJBGCFK
