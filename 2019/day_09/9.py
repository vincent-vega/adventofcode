#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from intcode import Intcode, Intcode_State


def _run(values: list, mode: int) -> int:
    state = Intcode_State(values, [ mode ])
    while not state.exit:
        Intcode.run(state)
    return state.output.pop() if state.output else None


def part1(values: list) -> int:
    return _run(values, 1)


def part2(values: list) -> int:
    return _run(values, 2)


if __name__ == '__main__':
    with open('input.txt') as f:
        values = list(map(int, f.read().split(',')))
    print(part1(values))  # 3512778005
    print(part2(values))  # 35920
