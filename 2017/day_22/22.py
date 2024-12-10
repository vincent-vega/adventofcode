#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import ceil

# direction: 0 up;    1 right;    2 down;     3 left
# state:     0 clean; 1 weakened; 2 infected; 3 flagged


def _forward(cur: tuple[int, int], direction: int) -> tuple[int, int]:
    x, y = cur
    x += -1 if direction == 3 else 1 if direction == 1 else 0
    y += -1 if direction == 0 else 1 if direction == 2 else 0
    return x, y


def _left(cur: tuple[int, int], direction: int) -> tuple[tuple[int, int], int]:
    direction = (direction - 1) % 4
    return _forward(cur, direction), direction


def _right(cur: tuple[int, int], direction: int) -> tuple[tuple[int, int], int]:
    direction = (direction + 1) % 4
    return _forward(cur, direction), direction


def _reverse(cur: tuple[int, int], direction: int) -> tuple[tuple[int, int], int]:
    direction = (direction + 2) % 4
    return _forward(cur, direction), direction


def part1(grid: set, cur: tuple[int, int], cnt: int) -> int:
    infected = 0
    cur_dir = 0
    for _ in range(cnt):
        if cur in grid:
            grid.remove(cur)
            cur, cur_dir = _right(cur, cur_dir)
        else:
            infected += 1
            grid.add(cur)
            cur, cur_dir = _left(cur, cur_dir)
    return infected


def part2(grid: dict, cur: tuple[int, int], cnt: int) -> int:
    infected = 0
    cur_dir = 0
    for _ in range(cnt):
        state = grid.get(cur, 0)
        grid[cur] = (state + 1) % 4
        if grid[cur] == 2:
            infected += 1
        if state == 1:
            cur = _forward(cur, cur_dir)
        else:
            cur, cur_dir = _left(cur, cur_dir) if state == 0 else _right(cur, cur_dir) if state == 2 else _reverse(cur, cur_dir)
    return infected


if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.read().splitlines()
        grid = { (x, y) for y, line in enumerate(lines, 1) for x, c in enumerate(line, 1) if c == '#' }
    start = ceil(len(lines[0]) / 2), ceil(len(lines) / 2)
    print(part1(set(grid), start, 10_000))  # 5196
    print(part2({ (x, y): 2 for x, y in grid }, start, 10_000_000))  # 2511633
