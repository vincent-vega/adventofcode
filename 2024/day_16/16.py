#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.lib import manhattan
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
            heapq.heappush(Q, (s + manhattan(*nxt, *E), s, *nxt, d))
    return -1


def part2(maze: set[tuple[int]], S: tuple[int], E: tuple[int]) -> int:
    Q = [(0, 0, *S, 1, { S })]
    history = {}  # (x, y), direction -> score
    best_score = None
    best_tiles = set()
    while Q:
        _, score, x, y, direction, visited = heapq.heappop(Q)
        for spin in (0, 1, -1):
            d = (direction + spin) % 4
            if (nxt := _nxt(x, y, d)) in maze:
                continue
            s = score + 1 + 1000 * abs(spin)

            if (nxt, d) not in history or history[nxt, d] > s:
                history[nxt, d] = s
            elif best_score and best_score < s:
                return len(best_tiles)
            elif history[nxt, d] < s:
                continue

            if nxt == E:
                if best_score is None:
                    best_score = s
                best_tiles |= visited | { E }
            else:
                heapq.heappush(Q, (s + manhattan(*nxt, *E), s, *nxt, d, visited | { nxt }))
    return len(best_tiles)


if __name__ == '__main__':
    with open('input.txt') as f:
        maze = set()
        for x, y, c in ((x, y, c) for y, line in enumerate(f) for x, c in enumerate(line)):
            if c == 'S':
                S = (x, y)
            elif c == 'E':
                E = (x, y)
            elif c == '#':
                maze.add((x, y))
    print(part1(maze, S, E))  # 88468
    print(part2(maze, S, E))  # 616
