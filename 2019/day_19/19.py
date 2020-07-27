#!/usr/bin/python3
# -*- coding: utf-8 -*-

from intcode import Intcode, Intcode_State


def _run(program: list, input_val: list) -> int:
    state = Intcode_State(program, input_val)
    while not state.exit:
        Intcode.run(state)
    return state.output.pop()


def part1(program: list, size: int) -> int:
    return len(set([ (x, y) for y in range(size) for x in range(size) if _run(program, [ x, y ]) == 1 ]))


def _check_line(program: list, slope: float, y: int, ship_size: int) -> bool:
    x = _get_point_x(program, slope, y, ship_size)
    return _run(program, [ x, y + ship_size - 1 ]) == 1


def _slope_factor(program: list, rowstart: int, meas_count: int, step: int) -> float:
    # factor = spaces / row
    accumulator = 0
    for y in range(rowstart, rowstart + meas_count * step, step):
        skip = int(y * (accumulator / int((y - rowstart + step) / step )) * 0.6)
        x = skip
        while _run(program, [ x, y ]) != 1:
            x += 1
        accumulator += x / y
    return accumulator / meas_count


def part2(program: list, ship_size: int) -> int:
    slope = _slope_factor(program, 10, 20, 2) * 1.2
    y = _bisect(program, slope, ship_size)
    x = _get_point_x(program, slope, y, ship_size)
    return x * 10**4 + y


def _bisect(program: list, slope: float, ship_size: int) -> int:
    low = 0
    high = _find_valid_y(program, slope, 50, 2000, ship_size)
    while high - low > 2:
        mid = low + int((high - low) / 2)
        if _check_line(program, slope, mid, ship_size):
            high = mid
        else:
            low = mid
    low += 1
    while not _check_line(program, slope, low, ship_size):
        low += 1
    return low


def _get_point_x(program: list, slope: float, y: int, ship_size: int) -> int:
    x = int(y * slope)
    while _run(program, [ x, y ]) == 1:
        x += 1
    return x - ship_size


def _find_valid_y(program: list, slope: float, start_y: int, step: int, ship_size: int) -> int:
    y = start_y
    while not _check_line(program, slope, y, ship_size):
        y += step
    return y


if __name__ == '__main__':
    with open('input.txt') as f:
        program = list(map(int, f.read().split(',')))
    print(part1(program, 50))  # 181
    print(part2(program, 100))  # 4240964
