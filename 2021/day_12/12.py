#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict, deque


def part1(cave: dict, small: set) -> int:
    cnt = 0
    D = deque([([ 'start' ], { 'start' })])
    while D:
        path, visited = D.popleft()
        last = path[-1]
        if last == 'end':
            cnt += 1
            continue
        for nxt in filter(lambda x: x not in small or x not in visited, cave[last]):
            D.append((path + [ nxt ], visited.union({ nxt }) if nxt in small else visited))
    return cnt


def _canvisit(visited: dict, small: set, nxt: str) -> bool:
    return nxt != 'start' and (nxt not in small or nxt not in visited or max(visited.values()) == 1)


def part2(cave: dict, small: set) -> int:
    cnt = 0
    D = deque([([ 'start' ], {})])
    while D:
        path, visited = D.popleft()
        last = path[-1]
        if last == 'end':
            cnt += 1
            continue
        for nxt in filter(lambda x: _canvisit(visited, small, x), cave[last]):
            if nxt in small:
                x = { nxt: visited[nxt] + 1 if nxt in visited else 1 }
            D.append((path + [ nxt ], {**visited, **x} if nxt in small else visited))
    return cnt


def _parse(lines: list) -> (dict, set):
    cave = defaultdict(set)
    small = set()
    for i, j in map(lambda s: s.split('-'), lines):
        cave[i].add(j)
        cave[j].add(i)
        if i not in small and all(c.islower() for c in i):
            small.add(i)
        if j not in small and all(c.islower() for c in j):
            small.add(j)
    return cave, small


if __name__ == '__main__':
    with open('input.txt') as f:
        cave, small = _parse(f.read().splitlines())
    print(part1(cave, small))  # 3576
    print(part2(cave, small))  # 84271
