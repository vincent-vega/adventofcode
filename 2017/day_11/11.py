#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def _move(cur: (int, int), direction: str) -> (int, int):
    x, y = cur
    if direction == 'nw':
        return x - 1, y + 0.5
    elif direction == 'n':
        return x, y + 1
    elif direction == 'ne':
        return x + 1, y + 0.5
    elif direction == 'se':
        return x + 1, y - 0.5
    elif direction == 's':
        return x, y - 1
    elif direction == 'sw':
        return x - 1, y - 0.5
    else:
        raise Exception('Invalid direction')


def _steps(cur: (int, int)) -> int:
    cnt = 0
    while cur != (0, 0):
        x, y = cur
        if x == 0:
            cur = (x, y + 1) if y < 0 else (x, y - 1)
        elif y == 0:
            cur = (x + 1, y + 0.5) if x < 0 else (x - 1, y + 0.5)
        else:
            x += 1 if x < 0 else -1
            y += 0.5 if y < 0 else -0.5
            cur = (x, y)
        cnt += 1
    return cnt


def part1(path: list) -> int:
    cur = (0, 0)
    for p in path:
        cur = _move(cur, p)
    return _steps(cur)


def part2(path: list) -> int:
    cur = (0, 0)
    M = 0
    for p in path:
        cur = _move(cur, p)
        M = max(M, _steps(cur))
    return M


if __name__ == '__main__':
    with open('input.txt') as f:
        path = ''.join(f.read().splitlines()).split(',')
    print(part1(path))  # 707
    print(part2(path))  # 1490
