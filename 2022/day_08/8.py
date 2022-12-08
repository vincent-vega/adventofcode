#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def _visible(grid: dict, x: int, y: int, X: int, Y: int) -> bool:
    h = grid[x, y]
    if all(grid[x, yy] < h for yy in range(0, y)):  # up
        return True
    if all(grid[x, yy] < h for yy in range(y + 1, Y + 1)):  # down
        return True
    if all(grid[xx, y] < h for xx in range(0, x)):  # left
        return True
    if all(grid[xx, y] < h for xx in range(x + 1, X + 1)):  # right
        return True
    return False


def part1(grid: dict) -> int:
    X = max(grid, key=lambda x: x[0])[0]
    Y = max(grid, key=lambda x: x[1])[1]
    edge = 2 * (X + 1) + 2 * (Y + 1) - 4
    return edge + sum(1 for x in range(1, X) for y in range(1, Y) if _visible(grid, x, y, X, Y))


def _shorter(grid: dict, h: int, coord: list[(int, int)]) -> int:
    for n, c in enumerate(coord, 1):
        if grid[c] >= h:
            return n
    return len(coord)


def _score(grid: dict, x: int, y: int, X: int, Y: int) -> int:
    h = grid[x, y]
    score = _shorter(grid, h, [ (x, Y) for Y in range(y - 1, -1, -1) ])  # up
    score *= _shorter(grid, h, [ (x, Y) for Y in range(y + 1, Y + 1) ])  # down
    score *= _shorter(grid, h, [ (X, y) for X in range(x - 1, -1, -1) ])  # left
    score *= _shorter(grid, h, [ (X, y) for X in range(x + 1, X + 1) ])  # right
    return score


def part2(grid: dict) -> int:
    X = max(grid, key=lambda x: x[0])[0]
    Y = max(grid, key=lambda x: x[1])[1]
    return max(_score(grid, x, y, X, Y) for x in range(1, X) for y in range(1, Y))


if __name__ == '__main__':
    with open('input.txt') as f:
        grid = { (x, y): int(h) for y, line in enumerate(f.read().splitlines()) for x, h in enumerate(line) }
    print(part1(grid))  # 1835
    print(part2(grid))  # 263670
