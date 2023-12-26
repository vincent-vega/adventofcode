#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from copy import deepcopy


def _load(rounded: dict[int, set[int]]) -> int:
    return sum(y * len(rocks) for y, rocks in rounded.items())


def _tilt(rounded: dict[int, set[int]], cubes: dict[int, set[int]], limit: int, reverse: bool = True) -> dict[int, set[int]]:
    for j in sorted(rounded, reverse=reverse):
        for i in set(rounded[j]):
            if reverse:
                for jj in range(j + 1, limit + 1):
                    if i in cubes[jj] or i in rounded[jj]:
                        J = jj - 1
                        break
                else:
                    J = limit
            else:
                for jj in range(j - 1, limit - 1, -1):
                    if i in cubes[jj] or i in rounded[jj]:
                        J = jj + 1
                        break
                else:
                    J = limit
            if J != j:
                rounded[j].remove(i)
                rounded[J].add(i)
    return rounded


def part1(rounded: dict[int, set[int]], cubes: dict[int, set[int]], max_y: int) -> int:
    return _load(_tilt(rounded, cubes, max_y))


def _rearrange(rounded: dict[int, set[int]]) -> dict[int, set[int]]:
    new = defaultdict(set)
    for i, value in rounded.items():
        for j in value:
            new[j].add(i)
    return new


def _serialize(rounded: dict[int, set[int]]) -> str:
    return '\n'.join([ f'{y}:' + '-'.join(map(str, sorted(rounded[y]))) for y in sorted(rounded) ])


def _deserialize(state: str) -> dict[int, set[int]]:
    return { int(y): { x for x in map(int, values.split('-')) } for y, values in map(lambda s: s.split(':'), state.split()) }


def _cycle(rounded: dict[int, set[int]], cubes_yx: dict[int, set[int]], cubes_xy: dict[int, set[int]], max_x: int, max_y: int) -> dict[int, set[int]]:
    rounded = _tilt(rounded, cubes_yx, max_y)  # north
    rounded = _tilt(_rearrange(rounded), cubes_xy, 0, False)  # west
    rounded = _tilt(_rearrange(rounded), cubes_yx, 1, False)  # south
    rounded = _tilt(_rearrange(rounded), cubes_xy, max_x)  # east
    return _rearrange(rounded)


def part2(rounded: dict[int, set[int]], cubes_yx: dict[int, set[int]], max_x: int, max_y: int, cycles: int) -> int:
    seen = set()
    history = list()
    cubes_xy = _rearrange(cubes_yx)
    for n in range(cycles):
        rounded = _cycle(rounded, cubes_yx, cubes_xy, max_x, max_y)
        state = _serialize(rounded)
        if state in seen:
            first_time = history.index(state)
            s = history[(cycles - first_time - 1) % (n - first_time) + first_time]
            return _load(_deserialize(s))
        seen.add(state)
        history.append(state)
    return _load(rounded)


def _parse(lines: list[str]) -> tuple[dict[int, set[int]], dict[int, set[int]]]:
    rounded = defaultdict(set)
    cubes = defaultdict(set)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                cubes[len(lines) - y].add(x)
            elif c == 'O':
                rounded[len(lines) - y].add(x)
    return rounded, cubes


if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.read().splitlines()
        rounded, cubes = _parse(lines)
    print(part1(deepcopy(rounded), cubes, len(lines)))  # 105249
    print(part2(rounded, cubes, len(lines[0]) - 1, len(lines), 1_000_000_000))  # 88680
