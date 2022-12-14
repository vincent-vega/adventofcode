#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque


def part1(stuff: set[(int, int)]) -> int:
    units = 0
    fallen = False
    lowest = max(y for _, y in stuff)
    while not fallen:
        cur_x, cur_y = 500, 0
        while True:
            if (cur_x, cur_y + 1) not in stuff:
                cur_y += 1
            elif (cur_x - 1, cur_y + 1) not in stuff:
                cur_x -= 1
                cur_y += 1
            elif (cur_x + 1, cur_y + 1) not in stuff:
                cur_x += 1
                cur_y += 1
            else:
                stuff.add((cur_x, cur_y))
                break
            if cur_y > lowest:
                fallen = True
                break
        if not fallen:
            units += 1
    return units


def part2(stuff: set[(int, int)]) -> int:
    units = 0
    bottom = max(y for _, y in stuff) + 2
    while (500, 0) not in stuff:
        cur_x, cur_y = 500, 0
        while True:
            if cur_y == bottom - 1:
                stuff.add((cur_x, cur_y))
                break
            elif (cur_x, cur_y + 1) not in stuff:
                cur_y += 1
            elif (cur_x - 1, cur_y + 1) not in stuff:
                cur_x -= 1
                cur_y += 1
            elif (cur_x + 1, cur_y + 1) not in stuff:
                cur_x += 1
                cur_y += 1
            else:
                stuff.add((cur_x, cur_y))
                break
        units += 1
    return units


def _wall(chunks: deque) -> set[(int, int)]:
    cur_x, cur_y = tuple(map(int, chunks.popleft().split(',')))
    rock = { (cur_x, cur_y) }
    while chunks:
        nxt_x, nxt_y = tuple(map(int, chunks.popleft().split(',')))
        if cur_x == nxt_x:
            rock.update((nxt_x, y) for y in range(min(cur_y, nxt_y), max(cur_y, nxt_y) + 1))
        elif cur_y == nxt_y:
            rock.update((x, nxt_y) for x in range(min(cur_x, nxt_x), max(cur_x, nxt_x) + 1))
        cur_x, cur_y = nxt_x, nxt_y
    return rock


if __name__ == '__main__':
    with open('input.txt') as f:
        rock = { (x, y) for line in f.read().splitlines() for x, y in _wall(deque(line.split(' -> '))) }
    print(part1(set(rock)))  # 715
    print(part2(rock))  # 25248
