#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from intcode import Intcode, Intcode_State


def _run(program: list, script: list) -> Intcode_State:
    state = Intcode_State(program, [ ord(x) for x in '\n'.join(script) ])
    while not state.exit:
        Intcode.run(state)
    return state


def part1(program: list) -> int:
    springscript = [
        # premature jump
        'NOT B J',
        'NOT C T',
        'OR T J',

        # premature jump landing
        'AND D T',
        'AND T J',

        # mandatory jump
        'NOT A T',
        'OR T J',

        'WALK\n' ]

    state = _run(program, springscript)
    return state.output.pop()


def part2(program: list) -> int:
    springscript = [
        # premature jump
        'NOT B T',
        'OR T J',
        'NOT C T',
        'OR T J',

        # premature jump landing
        'AND D J',
        # potential next jump landing
        'AND H J',

        # mandatory jump
        'NOT A T',
        'OR T J',

        'RUN\n' ]

    state = _run(program, springscript)
    return state.output.pop()


if __name__ == '__main__':
    with open('input.txt') as f:
        program = list(map(int, f.read().split(',')))
    print(part1(program))  # 19354890
    print(part2(program))  # 1140664209
