#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.lib import adj


def _score(heights: dict[tuple[int, int], int], start: tuple[int, int]) -> int:
    score = 0
    visited = set()
    D = [ (start, 0) ]
    while D:
        cur, n = D.pop()
        for nxt in (nxt for nxt in adj(*cur) if nxt in heights and heights[nxt] == n + 1):
            if heights[nxt] == 9 and nxt not in visited:
                score += 1
                visited.add(nxt)
            else:
                D.append((nxt, n + 1))
    return score


def _rating(heights: dict[tuple[int, int], int], start: tuple[int, int]) -> int:
    score = 0
    seen = set()
    D = [ (start, 0, [ start ]) ]
    while D:
        cur, n, path = D.pop()
        for nxt in (nxt for nxt in adj(*cur) if nxt in heights and heights[nxt] == n + 1):
            path.append(nxt)
            if heights[nxt] == 9 and tuple(path) not in seen:
                score += 1
                seen.add(tuple(path))
            else:
                D.append((nxt, n + 1, path))
    return score


def part1(heights: dict[tuple[int, int], int]) -> int:
    return sum(_score(heights, c) for c, h in heights.items() if h == 0)


def part2(heights: dict[tuple[int, int], int]) -> int:
    return sum(_rating(heights, c) for c, h in heights.items() if h == 0)


if __name__ == '__main__':
    with open('input.txt') as f:
        heights = { (x, y): h for y, line in enumerate(f.read().splitlines()) for x, h in enumerate(map(int, line)) }
    print(part1(heights))  # 582
    print(part2(heights))  # 1302
