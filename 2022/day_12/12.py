#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import heapq


def _adj(world: dict, cur: (int, int)) -> list:
    x, y = cur
    return [ (x + dx, y + dy) for dx, dy in [ (-1, 0), (1, 0), (0, -1), (0, 1) ] if (x + dx, y + dy) in world ]


def part1(world: dict, start: (int, int), end: (int, int)) -> int:
    return _count(world, start, end)


def _count(world: dict, start: (int, int), end: (int, int)) -> int:
    x, y = start
    Q = [(0, x, y)]
    visited = set()
    while Q:
        steps, x, y = heapq.heappop(Q)
        steps += 1
        for xx, yy in ( nxt for nxt in _adj(world, (x, y)) if nxt not in visited and (world[nxt] - world[x, y]) < 2 ):
            if (xx, yy) == end:
                return steps
            visited.add((xx, yy))
            heapq.heappush(Q, (steps, xx, yy))
    return -1


def part2(world: dict, end: (int, int)) -> int:
    return min(filter(lambda n: n > 0, ( _count(world, (x, y), end) for (x, y), h in world.items() if h == 0 )))


def _height(h: str) -> int:
    if h == 'S':
        return 0
    elif h == 'E':
        return ord('z') - ord('a')
    return ord(h) - ord('a')


if __name__ == '__main__':
    with open('input.txt') as f:
        world = {}
        for y, line in enumerate(f.read().splitlines()):
            for x, h in enumerate(line):
                world[(x, y)] = _height(h)
                if h == 'S':
                    S = (x, y)
                elif h == 'E':
                    E = (x, y)
    print(part1(world, S, E))  # 447
    print(part2(world, E))  # 446
