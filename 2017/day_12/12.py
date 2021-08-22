#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def _parse(line: str) -> set:
    _, ids = line.split(' <-> ')
    return { int(i) for i in ids.split(', ') }


def _scan(programs: dict, seen: set, target: int=0) -> set:
    seen.add(target)
    group = set([ target ])
    to_scan = programs[target] - seen
    group.update(to_scan)
    group.update({ nn for n in to_scan for nn in _scan(programs, seen, n) })
    return group


def part1(programs: dict) -> int:
    return len(_scan(programs, {0}, 0))


def part2(programs: dict) -> int:
    groups = []
    left = set(programs.keys())
    while left:
        p = left.pop()
        g = _scan(programs, {p}, p)
        left -= g
        groups.append(g)
    return len(groups)


if __name__ == '__main__':
    with open('input.txt') as f:
        programs = { n: _parse(x) for n, x in enumerate(f.read().splitlines()) }
    print(part1(programs))  # 283
    print(part2(programs))  # 195
