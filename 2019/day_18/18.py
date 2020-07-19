#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict, namedtuple, deque
import re


def _get_directions(coord: (int, int)) -> tuple:
    x, y = coord
    return (x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)


def part1(M: dict) -> int:
    keys = [ k for k in M.keys() if re.match(r'[a-z]', M[k]) ]
    start = next(filter(lambda k: M[k] == '@', M.keys()))
    KeyFinder = namedtuple('KeyFinder', 'coord keys path_current')
    Q = deque([ KeyFinder(start, set(), []) ])
    history = set()
    while Q:
        cur = Q.popleft()
        state = (cur.coord, tuple(sorted(cur.keys)))
        if state in history:
            continue
        history.add(state)
        cur.path_current.append(cur.coord)
        curr_char = M[cur.coord]
        if re.match(r'[a-z]', curr_char) and curr_char not in cur.keys:
            cur.keys.add(curr_char)
            if len(cur.keys) == len(keys):
                return len(cur.path_current) - 1
        elif re.match(r'[A-Z]', curr_char):
            key_name = chr(ord(curr_char) + 32)
            if key_name not in cur.keys:
                continue
        for child in filter(lambda d: d in M.keys(), _get_directions(cur.coord)):
            Q.append(KeyFinder(child, set(cur.keys), list(cur.path_current)))


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
