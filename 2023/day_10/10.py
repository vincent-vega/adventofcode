#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict


def _navigate(pipe: dict[tuple[int], list[tuple[int]]], cur: tuple[int, int], end: tuple[int, int]) -> set[tuple[int]]:
    last = end
    nodes = set([ cur ])
    while cur != end:
        if cur not in pipe:
            return None
        edge1, edge2 = pipe[cur]
        if last != edge1 and last != edge2:
            return None
        cur, last = edge1 if edge2 == last else edge2, cur
        nodes.add(cur)
    return nodes


def _loop(pipe: dict[tuple[int], list[tuple[int]]], start: tuple[int]) -> set[tuple[int]]:
    x, y = start
    for s in _to('S', x, y):
        if (loop := _navigate(pipe, s, start)) is not None:
            return loop


def part1(pipe: dict[tuple[int], list[tuple[int]]], start: tuple[int]) -> int:
    return len(loop) // 2 if len(loop := _loop(pipe, start)) % 2 == 0 else (len(loop) // 2 + 1)


def _raycast(loop: set[tuple[int]], symbols: dict[tuple[int], str], min_x: int, x: int, y: int) -> int:
    if not (X := [ symbols[x, y] for x in range(min_x - 1, x + 1) if (x, y) in loop and symbols[x, y] != '-']):
        return 0
    count = 1
    for i in range(1, len(X)):
        if X[i - 1] in { '|', 'J', '7' }:
            count += 1
        elif X[i - 1] == 'L' and X[i] == 'J':
            count += 1
        elif X[i - 1] == 'F' and X[i] == '7':
            count += 1
    return count


def part2(pipe: dict[tuple[int], list[tuple[int]]], symbols: dict[tuple[int], str], start: tuple[int]) -> int:
    loop = _loop(pipe, start)
    count = 0
    min_x = min(x for x, _ in loop)
    for x in range(min_x, max(x for x, _ in loop) + 1):
        for y in range(min(y for _, y in loop), max(y for _, y in loop) + 1):
            if (x, y) in loop:
                continue
            if (v := _raycast(loop, symbols, min_x, x, y)) > 0 and v % 2 != 0:
                count += 1
    return count


def _to(symbol: str, x: int, y: int) -> tuple[tuple[int]]:
    if symbol == '|':
        return (x, y + 1), (x, y - 1)
    elif symbol == '-':
        return (x + 1, y), (x - 1, y)
    elif symbol == 'L':
        return (x + 1, y), (x, y - 1)
    elif symbol == 'J':
        return (x - 1, y), (x, y - 1)
    elif symbol == '7':
        return (x - 1, y), (x, y + 1)
    elif symbol == 'F':
        return (x + 1, y), (x, y + 1)
    return (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)


def _parse(lines: list[str]) -> tuple[dict, tuple[int]]:
    pipe = defaultdict(list)
    symbols = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c != '.':
                symbols[x, y] = c
                pipe[x, y].extend(_to(c, x, y))
                if c == 'S':
                    start = (x, y)
    sx, sy = start
    if (sx, sy - 1) in pipe and (sx, sy + 1) in pipe:
        symbols[start] = '|'
    elif (x + 1, y) in pipe and (x - 1, y) in pipe:
        symbols[start] = '-'
    elif (x + 1, y) in pipe and (x, y - 1) in pipe:
        symbols[start] = 'L'
    elif (x - 1, y) in pipe and (x, y - 1) in pipe:
        symbols[start] = 'J'
    elif (x - 1, y) in pipe and (x, y + 1) in pipe:
        symbols[start] = '7'
    elif (x + 1, y) in pipe and (x, y + 1) in pipe:
        symbols[start] = 'F'
    return pipe, symbols, start


if __name__ == '__main__':
    with open('input.txt') as f:
        pipe, symbols, start = _parse(f.read().splitlines())
    print(part1(pipe, start))  # 6640
    print(part2(pipe, symbols, start))  # 411
