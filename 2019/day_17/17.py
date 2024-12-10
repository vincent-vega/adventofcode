#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from intcode import Intcode, Intcode_State


def _parse(view: list) -> set:
    M = set()
    row_count = 0
    for row in ''.join(view).split('\n'):
        for col in range(len(row)):
            if row[col] == '#':
                M.add((col, row_count))
        row_count += 1
    return M


def part1(program: list) -> int:
    state = Intcode_State(program)
    while not state.exit:
        Intcode.run(state)
    M = _parse([ chr(x) for x in state.output ])

    def _is_xsection(coord: tuple[int, int]) -> bool:
        x, y = coord
        return (x, y - 1) in M and (x, y + 1) in M and (x - 1, y) in M and (x + 1, y) in M

    return sum([ x * y for x, y in filter(_is_xsection, M) ])


def part2(program: list) -> int:
    main = 'A,B,B,A,B,C,A,C,B,C\n'
    a = 'L,4,L,6,L,8,L,12\n'
    b = 'L,8,R,12,L,12\n'
    c = 'R,12,L,6,L,6,L,8\n'
    tot = main + a + b + c + 'n\n'
    state = Intcode_State(program, [ ord(c) for c in tot ])
    while not state.exit:
        Intcode.run(state)
    return state.output.pop()


if __name__ == '__main__':
    with open('input.txt') as f:
        values = list(map(int, f.read().split(',')))
    print(part1(values))  # 6448
    print(part2([ 2 ] + values[1:]))  # 914900
