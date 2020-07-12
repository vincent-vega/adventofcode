#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from intcode import Intcode, Intcode_State


def _rotate(current_coord: (int, int), current_dir: str, operation: int) -> ((int, int), str):
    LEFT_90 = 0
    # RIGHT_90 = 1
    x_offs = y_offs = 0
    if current_dir == '^':
        new_dir = '<' if operation == LEFT_90 else '>'
        x_offs = -1 if operation == LEFT_90 else 1
    elif current_dir == '<':
        new_dir = 'v' if operation == LEFT_90 else '^'
        y_offs = -1 if operation == LEFT_90 else 1
    elif current_dir == '>':
        new_dir = '^' if operation == LEFT_90 else 'v'
        y_offs = 1 if operation == LEFT_90 else -1
    else:  # current_dir == 'v'
        new_dir = '>' if operation == LEFT_90 else '<'
        x_offs = 1 if operation == LEFT_90 else -1
    return (current_coord[0] + x_offs, current_coord[1] + y_offs), new_dir


def _run(values: list, current_color: int) -> dict:
    BLACK = 0  # WHITE = 1
    current_position = (0, 0)
    current_direction = '^'
    outputs = [ None, '^' ]
    output_idx = 0

    def _get_new_col(out: list) -> str:
        return out[0]

    def _get_new_oper(out: list) -> str:
        return out[1]

    panels = { current_position: current_color }
    state = Intcode_State(values, [ current_color ])
    while not state.exit:
        Intcode.run(state)
        if state.output:
            outputs[output_idx] = state.output.pop()
            if output_idx == 0:
                # color output
                panels[current_position] = _get_new_col(outputs)
            else:
                # direction output
                current_position, current_direction = _rotate(current_position, current_direction, _get_new_oper(outputs))
                if current_position not in panels:
                    panels[current_position] = BLACK
            output_idx = (output_idx + 1) % len(outputs)
        if state.input_req:
            state.input.append(panels[current_position])
    return panels


def _draw(c: int) -> str:
    BLACK = 0
    return ' ' if c == BLACK else '#'


def part1(values: list) -> int:
    return len(_run(values, 0))


def part2(values: list) -> str:
    panels = _run(values, 1)
    max_Y = max(panels.keys(), key=lambda k: k[1])[1]
    min_X = min(panels.keys(), key=lambda k: k[0])[0]
    s = ''
    for y in range(max_Y, max_Y - len(panels.keys()), -1):
        row = sorted([ x for x in panels.keys() if x[1] == y ], key=lambda k: k[0])
        if len(row) > 0:
            max_x_in_row = max(row, key=lambda c: c[0])[0]
            s += ''.join([ _draw(panels[(x, y)] if (x, y) in panels else ' ') for x in range(min_X, max_x_in_row) ]) + '\n'
    return s


if __name__ == '__main__':
    with open('input.txt') as f:
        values = list(map(int, f.read().split(',')))
    print(part1(values))  # 2336
    print(part2(values))  # UZAEKBLP
