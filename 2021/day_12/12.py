#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict


def part1(cave: dict, small: set) -> int:
    cnt = 0
    Q = [('start', { 'start' })]
    while Q:
        last, visited = Q.pop()
        if last == 'end':
            cnt += 1
            continue
        for nxt in filter(lambda x: x not in small or x not in visited, cave[last]):
            Q.append((nxt, visited.union({ nxt }) if nxt in small else visited))
    return cnt


def _canvisit(visited: dict, small: set, nxt: str, visited_twice: bool) -> bool:
    return nxt != 'start' and (nxt not in small or nxt not in visited or not visited_twice)


def part2(cave: dict, small: set) -> int:
    cnt = 0
    Q = [('start', set([ 'start' ]), False)]
    while Q:
        last, visited, visited_twice = Q.pop()
        if last == 'end':
            cnt += 1
            continue
        for nxt in filter(lambda x: _canvisit(visited, small, x, visited_twice), cave[last]):
            Q.append((nxt, visited.union({ nxt }) if nxt in small else visited, visited_twice or nxt in visited))
    return cnt


def _parse(lines: list) -> (dict, set):
    cave = defaultdict(set)
    small = set()
    for i, j in map(lambda s: s.split('-'), lines):
        cave[i].add(j)
        cave[j].add(i)
        if i not in small and i.islower():
            small.add(i)
        if j not in small and j.islower():
            small.add(j)
    return cave, small


if __name__ == '__main__':
    with open('input.txt') as f:
        cave, small = _parse(f.read().splitlines())
    print(part1(cave, small))  # 3576
    print(part2(cave, small))  # 84271
