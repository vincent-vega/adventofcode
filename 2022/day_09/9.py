#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def _move(start: (int, int), delta: (int, int)) -> (int, int):
    x, y = start
    dx, dy = delta
    return (x + dx, y + dy)


def _stay(k1: (int, int), k2: (int, int)) -> bool:
    x1, y1 = k1
    x2, y2 = k2
    return max(abs(x2 - x1), abs(y2 - y1)) < 2  # Chebyshev distance


def _tail_seen(motions: ((int, int), int), length: int) -> set[(int, int)]:
    knots = [ (0, 0) ] * length
    seen = { (0, 0) }
    for delta, steps in motions:
        for _ in range(steps):
            knots[0] = _move(knots[0], delta)
            for n in range(1, length):
                if _stay(knots[n - 1], knots[n]):
                    continue
                lead_x, lead_y = knots[n - 1]
                x, y = knots[n]
                if lead_y == y:
                    x += 1 if lead_x > x else - 1
                elif lead_x == x:
                    y += 1 if lead_y > y else - 1
                else:
                    x += 1 if lead_x > x else - 1
                    y += 1 if lead_y > y else - 1
                knots[n] = (x, y)
            seen.add(knots[-1])
    return seen


def part1(motions: ((int, int), int)) -> int:
    return len(_tail_seen(motions, 2))


def part2(motions: ((int, int), int)) -> int:
    return len(_tail_seen(motions, 10))


if __name__ == '__main__':
    with open('input.txt') as f:
        D = { 'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0) }
        motions = [ (D[x[0]], int(x[1])) for x in map(str.split, f.read().splitlines()) ]
    print(part1(motions))  # 6357
    print(part2(motions))  # 2627
