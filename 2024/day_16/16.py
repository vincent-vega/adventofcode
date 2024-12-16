#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.lib import _print, _manhattan
import heapq

def _nxt(x: int, y: int, d: int) -> tuple[int]:
    if d == 0:
        return x, y - 1
    elif d == 1:
        return x + 1, y
    elif d == 2:
        return x, y + 1
    elif d == 3:
        return x - 1, y


def part1(maze: set[tuple[int]], S: tuple[int], E: tuple[int]) -> int:
    Q = [(0, 0, *S, 1)]
    history = {}  # (x, y), direction -> score
    while Q:
        _, score, x, y, direction = heapq.heappop(Q)
        for spin in (0, 1, -1):
            d = (direction + spin) % 4
            if (nxt := _nxt(x, y, d)) in maze:
                continue
            s = score + 1 + 1000 * abs(spin)

            if (nxt, d) not in history or history[nxt, d] > s:
                history[nxt, d] = s
            elif history[nxt, d] < s:
                continue

            if nxt == E:
                return s
            heapq.heappush(Q, (s + _manhattan(*nxt, *E), s, *nxt, d))
    return -1


def part2(values):
    pass


def _parse(file):
    with open(file) as f:
        maze = set()
        for x, y, c in ((x, y, c) for y, line in enumerate(f) for x, c in enumerate(line)):
            if c == 'S':
                S = (x, y)
            elif c == 'E':
                E = (x, y)
            elif c == '#':
                maze.add((x, y))
    return maze, S, E


# import pudb; pu.db
if __name__ == '__main__':
    maze, S, E = _parse('input.txt')
    print(part1(maze, S, E))  # 88468
    # _print(part2(values))  #
