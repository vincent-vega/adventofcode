#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import system

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

def _run(values: list, state: dict, input_val: list) -> list:
    out = []
    while not state['exit']:
        state = _run_op(state, input_val)
        if state['output'] is not None:
            out.append(state['output'])
            state['output'] = None
    #print(f'OUT => {out}')
    return out

def part1(values: list) -> int:
    state = {
        'values': list(values),
        'instruction_ptr': 0,
        'exit': False,
        'output': None,
        'relative_base': 0
    }
    out = _run(values, state, [])
    return sum([ 1 if out[i] == 2 else 0 for i in range(2, len(out), 3) ])

class Tile:

    x: int
    y: int
    tile_id: int

    def __init__(self, x, y, tile_id):
        self.x = x
        self.y = y
        self.tile_id = tile_id

def _print_screen(out: list) -> str:
    #system('clear')
    screen = ''
    for i in range(0, len(out), 3):
        if i > 0 and out[i] == 0:
            screen += '\n'
        tile = ' '
        if out[i + 2] == 1:
            tile = '#'
        elif out[i + 2] == 2:
            tile = '*'
        elif out[i + 2] == 3:
            tile = '='
        elif out[i + 2] == 4:
            tile = 'O'
        screen += tile
    return screen

def _get_elems(out: list) -> (list, list):
    return sorted([ t for t in  [ out[i:i + 3] for i in range(0, len(out), 3) ] if t[2] > 2 ], key=lambda t: t[2])

def part2(values: list) -> int:
    state = {
        'values': list(values),
        'instruction_ptr': 0,
        'exit': False,
        'output': None,
        'relative_base': 0
    }
    out = _run(list(values), state, [ 2 ])
    paddle_p, ball_p = _get_elems(out)
    paddle = paddle_p
    ball = ball_p
    for _ in range(10):
        print(_print_screen(out))
        joystick = 1 if paddle[0] < ball[0] else -1 if paddle[0] > ball[0] else 0
        out = _run(list(values), state, [ 2 ])
        a = _get_elems(out)
        #print(a)
        paddle, ball = a[0], a[1]

    #print(f'paddlex {paddle[0]} ballx {ball[0]}')

if __name__ == '__main__':
    with open('input.txt') as f:
        values = list(map(int, f.read().split(',')))
    print(part1(values)) # 286
    #print(part2(values)) #

