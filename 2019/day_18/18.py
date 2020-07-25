#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict, namedtuple, deque
import re


def part1(M: dict) -> int:
    keys = [ k for k in M.keys() if _is_key(M[k]) ]
    start = next(filter(lambda k: M[k] == '@', M.keys()))
    KeyFinder = namedtuple('KeyFinder', [ 'coord', 'keys', 'steps' ])
    Q = deque([ KeyFinder(start, set(), 0) ])
    history = set()
    while Q:
        cur = Q.popleft()
        state = (cur.coord, tuple(sorted(cur.keys)))
        if state in history:
            continue
        history.add(state)
        curr_char = M[cur.coord]
        if _is_key(curr_char) and curr_char not in cur.keys:
            cur.keys.add(curr_char)
            if len(cur.keys) == len(keys):
                return cur.steps
        elif _is_door(curr_char):
            need_key = curr_char.swapcase()
            if need_key not in cur.keys:
                continue
        for coord in filter(lambda d: d in M.keys(), _get_adj_coord(cur.coord)):
            Q.append(KeyFinder(coord, set(cur.keys), cur.steps + 1))
    return -1


def _is_key(char: str) -> bool:
    return re.match(r'[a-z]', char)


def _is_door(char: str) -> bool:
    return re.match(r'[A-Z]', char)


def _get_adj_coord(coord: (int, int)) -> tuple:
    x, y = coord
    return (x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)


def _parse(values: list) -> dict:
    M = defaultdict(str)
    for y in range(len(values)):
        for x in range(len(values[y])):
            if values[y][x] != '#':
                M[(x, y)] = values[y][x]
    return M


if __name__ == '__main__':
    with open('input.txt') as f:
        values = f.read().splitlines()
    print(part1(_parse(values)))  # 4620
