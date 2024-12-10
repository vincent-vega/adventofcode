#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import heapq


def _adj(x: int, y: int) -> set:
    return { (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1) }


def _valid(current: tuple[int, int], bottom_right: tuple[int, int]) -> bool:
    x, y = current
    X, Y = bottom_right
    return X >= x >= 0 <= y <= Y


def _risk(risk: dict, X: int, Y: int, x: int, y: int) -> int:
    n = risk[x % X, y % Y] + x // X + y // Y
    return 9 if n % 9 == 0 else n % 9


def _lowest(risk: dict, replication_factor: int) -> int:
    visited = set()
    Q = [(0, 0, 0)]
    X, Y = map(lambda x: x + 1, max(risk))
    target = (X * replication_factor - 1, Y * replication_factor - 1)
    while Q:
        steps, x, y = heapq.heappop(Q)
        for x, y in filter(lambda coord: coord not in visited and _valid(coord, target), _adj(x, y)):
            count = steps + _risk(risk, X, Y, x, y)
            if (x, y) == target:
                return count
            visited.add((x, y))
            heapq.heappush(Q, (count, x, y))


def part1(risk: dict) -> int:
    return _lowest(risk, 1)


def part2(risk: dict, n: int) -> int:
    return _lowest(risk, n)


if __name__ == '__main__':
    with open('input.txt') as f:
        risk = { (x, y): int(c) for y, line in enumerate(f.read().split()) for x, c in enumerate(line) }
    print(part1(risk))  # 415
    print(part2(risk, 5))  # 2864
