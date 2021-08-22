#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def _scan(programs: dict, seen: set, target: int) -> set:
    seen.add(target)
    group = { target }
    to_scan = programs[target] - seen
    group.update(to_scan)
    group.update({ nn for n in to_scan for nn in _scan(programs, seen, n) })
    return group


def part1(programs: dict) -> int:
    return len(_scan(programs, {0}, 0))


def part2(programs: dict) -> int:
    cnt = 0
    left = set(programs.keys())
    while left:
        p = left.pop()
        g = _scan(programs, {p}, p)
        left -= g
        cnt += 1
    return cnt


if __name__ == '__main__':
    with open('input.txt') as f:
        programs = { int(k): { int(x) for x in v.split(', ') } for k, v in map(lambda l: l.split(' <-> '), f.read().splitlines()) }
    print(part1(programs))  # 283
    print(part2(programs))  # 195
