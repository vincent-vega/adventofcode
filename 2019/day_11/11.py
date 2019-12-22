#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def _run_op(state: dict, input_values: list) -> dict:
    POSITION_MODE  = 0
    IMMEDIATE_MODE = 1
    RELATIVE_MODE  = 2
    instruction_ptr = state['instruction_ptr']
    values = state['values']
    instruction = values[instruction_ptr]
    def _resize(mem, num):
        mem.extend([ 0 for _ in range(num) ])
    def _check_resize(mem, addr):
        if addr > len(mem) - 1:
            _resize(mem, addr - len(mem) + 1)
    def _read_value(state, i, m):
        v = state['values']
        base = state['relative_base']
        if m == IMMEDIATE_MODE:
            return v[i]
        addr = v[i] if m == POSITION_MODE else base + v[i]
        _check_resize(v, addr)
        return v[addr]
    def _write_value(state, i, value, m):
        v = state['values']
        base = state['relative_base']
        assert m == POSITION_MODE or m == RELATIVE_MODE
        addr = v[i] if m == POSITION_MODE else base + v[i]
        _check_resize(v, addr)
        v[addr] = value
    def _add(state, i, m1, m2, m3):
        v1 = _read_value(state, i + 1, m1)
        v2 = _read_value(state, i + 2, m2)
        _write_value(state, i + 3, v1 + v2, m3)
        state['instruction_ptr'] = i + 4
        return state
    def _mul(state, i, m1, m2, m3):
        v = state['values']
        v1 = _read_value(state, i + 1, m1)
        v2 = _read_value(state, i + 2, m2)
        _write_value(state, i + 3, v1*v2, m3)
        state['instruction_ptr'] = i + 4
        return state
    def _set(state, i, m1, _, __):
        _write_value(state, i + 1, input_values.pop(), m1)
        state['instruction_ptr'] = i + 2
        return state
    def _out(state, i, m1, _, __):
        state['instruction_ptr'] = i + 2
        state['output'] = _read_value(state, i + 1, m1)
        return state
    def _jump_true(state, i, m1, m2, _):
        v1 = _read_value(state, i + 1, m1)
        v2 = _read_value(state, i + 2, m2)
        state['instruction_ptr'] = v2 if v1 != 0 else i + 3
        return state
    def _jump_false(state, i, m1, m2, _):
        v1 = _read_value(state, i + 1, m1)
        v2 = _read_value(state, i + 2, m2)
        state['instruction_ptr'] = v2 if v1 == 0 else i + 3
        return state
    def _less_than(state, i, m1, m2, m3):
        v1 = _read_value(state, i + 1, m1)
        v2 = _read_value(state, i + 2, m2)
        _write_value(state, i + 3, 1 if v1 < v2 else 0, m3)
        state['instruction_ptr'] = i + 4
        return state
    def _equals(state, i, m1, m2, m3):
        v1 = _read_value(state, i + 1, m1)
        v2 = _read_value(state, i + 2, m2)
        _write_value(state, i + 3, 1 if v1 == v2 else 0, m3)
        state['instruction_ptr'] = i + 4
        return state
    def _adjust_base(state, i, m1, _, __):
        state['relative_base'] += _read_value(state, i + 1, m1)
        state['instruction_ptr'] = i + 2
        return state
    def _exit(*argv):
        state['exit'] = True
        return state
    def _get_opcode(instr):
        return instr%100
    def _get_mode(instr):
        return instr//100%10, instr//1000%10, instr//10000
    return {
        1:  _add,
        2:  _mul,
        3:  _set,
        4:  _out,
        5:  _jump_true,
        6:  _jump_false,
        7:  _less_than,
        8:  _equals,
        9:  _adjust_base,
        99: _exit
    }[_get_opcode(instruction)](state, instruction_ptr, *_get_mode(instruction))

def _rotate(current_coord: (int, int), current_dir: str, operation: int) -> ((int, int), str):
    LEFT_90  = 0
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
    else: # current_dir == 'v'
        new_dir = '>' if operation == LEFT_90 else '<'
        x_offs = 1 if operation == LEFT_90 else -1
    return (current_coord[0] + x_offs, current_coord[1] + y_offs), new_dir

def _run(values: list, current_color: int) -> dict:
    state = {
        'values': list(values),
        'instruction_ptr': 0,
        'exit': False,
        'output': None,
        'relative_base': 0
    }
    BLACK = 0
    # WHITE = 1

    current_position = (0,0)
    current_direction = '^'

    outputs = [ None, '^' ]
    output_idx = 0
    def _get_new_col(out: list) -> str:
        return out[0]
    def _get_new_oper(out: list) -> str:
        return out[1]

    panels = { current_position: current_color }
    while not state['exit']:
        state = _run_op(state, [ panels[current_position] ])
        outputs[output_idx] = state['output']
        if state['output'] is not None:
            if output_idx == 0:
                # COLOR OUTPUT
                panels[current_position] = _get_new_col(outputs)
            else:
                # DIRECTION OUTPUT
                current_position, current_direction = _rotate(current_position, current_direction, _get_new_oper(outputs))
                if current_position not in panels:
                    panels[current_position] = BLACK
            output_idx = (output_idx + 1)%len(outputs)
            state['output'] = None
    return panels

def _draw(c: (int, int)) -> str:
    BLACK = 0
    return ' ' if c == BLACK else '#'

def part1(values: list) -> int:
    return len(_run(values, 0))

def part2(values: list) -> int:
    panels = _run(values, 1)
    max_Y = max(panels.keys(), key=lambda k: k[1])[1]
    min_X = min(panels.keys(), key=lambda k: k[0])[0]
    s = ''
    for y in range(max_Y, max_Y - len(panels.keys()), -1):
        row = sorted([ x for x in panels.key() if x[1] == y ], key=lambda k: k[0])
        if len(row) > 0:
            max_x_in_row = max(row, key=lambda c: c[0])[0]
            s += ''.join([ _draw(panels[(x, y)] if (x, y) in panels else ' ') for x in range(min_X, max_x_in_row) ]) + '\n'
    return s

if __name__ == '__main__':
    with open('input.txt') as f:
        values = list(map(int, f.read().split(',')))
    print(part1(values)) # 2336
    print(part2(values)) # UZAEKBLP

