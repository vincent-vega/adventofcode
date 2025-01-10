#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.lib import manhattan, adj
import heapq


def _escape(walls: set[tuple[int, int]], X: int, Y: int) -> int:
    Q = [(0, 0, 0, 0)]
    visited = set()
    while Q:
        _, steps, x, y = heapq.heappop(Q)
        if (x, y) in visited:
            continue
        if (x, y) == (X, Y):
            return steps
        visited.add((x, y))
        steps += 1
        for xx, yy in ((xx, yy) for xx, yy in adj(x, y) if (xx, yy) not in visited and 0 <= xx <= X and 0 <= yy <= Y and (xx, yy) not in walls):
            heapq.heappush(Q, (steps + manhattan(xx, yy, X, Y), steps, xx, yy))
    return -1


def part1(memory: list[tuple[int, int]], X: int, Y: int, N: int) -> int:
    return _escape({ memory[n] for n in range(N) }, X, Y)


def part2(memory: list[tuple[int, int]], X: int, Y: int, count: int) -> str:
    walls = { memory[n] for n in range(count) }
    while count < len(memory):
        if _escape(walls, X, Y) < 0:
            x, y = memory[count - 1]
            return f'{x},{y}'
        walls.add(memory[count])
        count += 1
    raise Exception('Always reachable')


if __name__ == '__main__':
    with open('input.txt') as f:
        memory = [ tuple(map(int, line.split(','))) for line in f ]
    print(part1(memory, 70, 70, 1024))  # 286
    print(part2(memory, 70, 70, 1024))  # 20,64
