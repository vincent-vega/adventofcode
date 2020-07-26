#!/usr/bin/python3
# -*- coding: utf-8 -*-

from intcode import Intcode, Intcode_State


def _run(program: list, input_val: list) -> int:
    state = Intcode_State(program, input_val)
    while not state.exit:
        Intcode.run(state)
    return state.output.pop()


def _get_beam(program: list, size: int) -> set:
    return set([ (x, y) for x in range(size) for y in range(size) if _run(program, [ y, x ]) == 1 ])


def part1(program: list, size: int) -> int:
    return len(_get_beam(program, size))


if __name__ == '__main__':
    with open('input.txt') as f:
        program = list(map(int, f.read().split(',')))
    print(part1(program, 50))  # 181
