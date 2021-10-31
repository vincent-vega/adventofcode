#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def _power_level(x: int, y: int, serial: int) -> int:
    rackID = x + 10
    digits = (rackID * y + serial) * rackID
    return 0 if digits < 100 else int(str(digits)[-3]) - 5


def _square_power(grid: dict, top_left: (int, int), square_size: int) -> int:
    X, Y = top_left
    return sum(grid[x, y] for y in range(Y, Y + square_size) for x in range(X, X + square_size))


def part1(grid: dict, grid_size: int, square_size: int) -> str:
    squares = { (x, y): _square_power(grid, (x, y), square_size) for y in range(1, grid_size - square_size + 1) for x in range(1, grid_size - square_size + 1) }
    top_left, _ = max(squares.items(), key=lambda item: item[1])
    return ','.join(map(str, top_left))


# _https://en.wikipedia.org/wiki/Summed-area_table
def _summered_area(grid: dict, grid_size: int) -> dict:
    summered_area_table = {}
    for y in range(grid_size, 0, -1):
        for x in range(grid_size, 0, -1):
            A = summered_area_table.get((x + 1, y + 1), 0)
            B = summered_area_table.get((x, y + 1), 0)
            C = summered_area_table.get((x + 1, y), 0)
            summered_area_table[x, y] = grid[x, y] - A + B + C
    return summered_area_table


def _square_value(summered_area_table: dict, square_size: int, x: int, y: int) -> int:
    A = summered_area_table.get((x + square_size, y + square_size), 0)
    B = summered_area_table.get((x, y + square_size), 0)
    C = summered_area_table.get((x + square_size, y), 0)
    D = summered_area_table[x, y]
    return D + A - B - C


def part2(grid: dict, grid_size: int) -> str:
    summered_area_table = _summered_area(grid, grid_size)
    top_left, max_value = max(grid.items(), key=lambda i: i[1])
    max_size = 1
    for square_size in range(2, grid_size + 1):
        for y in range(grid_size - square_size + 1, 0, -1):
            for x in range(grid_size - square_size + 1, 0, -1):
                v = _square_value(summered_area_table, square_size, x, y)
                if v > max_value:
                    max_value = v
                    top_left = (x, y)
                    max_size = square_size
    return ','.join(map(str, list(top_left) + [ max_size ]))


if __name__ == '__main__':
    grid = { (x, y): _power_level(x, y, 7165) for y in range(1, 301) for x in range(1, 301) }
    print(part1(grid, 300, 3))  # 235,20
    print(part2(grid, 300))  # 237,223,14
