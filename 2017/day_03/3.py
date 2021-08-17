#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def _square_coord(square: int) -> (int, int):
    max_steps, step_cnt = 1, 1
    direction = 0  # 0: RIGHT, 1: UP, 2: LEFT, 3: DOWN
    x, y = 0, 0
    for _ in range(2, square + 1):
        step_cnt -= 1
        x += 1 if direction == 0 else -1 if direction == 2 else 0
        y += 1 if direction == 1 else -1 if direction == 3 else 0
        if step_cnt == 0:
            direction = (direction + 1) % 4
            if direction == 2 or direction == 0:
                max_steps += 1
            step_cnt = max_steps
    return x, y


def part1(square: int) -> int:
    return sum(map(abs, _square_coord(square)))


def _adj(x: int, y: int) -> list:
    return [ (x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0) ]


def part2(square: int) -> int:
    max_steps, step_cnt = 1, 1
    direction = 0  # 0: RIGHT, 1: UP, 2: LEFT, 3: DOWN
    x, y = 0, 0
    mem = { (0, 0): 1 }
    for _ in range(2, square + 1):
        step_cnt -= 1
        x += 1 if direction == 0 else -1 if direction == 2 else 0
        y += 1 if direction == 1 else -1 if direction == 3 else 0
        S = sum(mem.get(c, 0) for c in _adj(x, y))
        if S > square:
            return S
        mem[(x, y)] = S
        if step_cnt == 0:
            direction = (direction + 1) % 4
            if direction == 2 or direction == 0:
                max_steps += 1
            step_cnt = max_steps
    raise Exception('Not found')


if __name__ == '__main__':
    print(part1(368078))  # 371
    print(part2(368078))  # 369601
