#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import system
from time import sleep

def _run_op(state: dict) -> dict:
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
        if len(state['input']) == 0:
            state['input_req'] = True
        else:
            _write_value(state, i + 1, state['input'].pop(), m1)
            state['instruction_ptr'] = i + 2
        return state
    def _out(state, i, m1, _, __):
        val = _read_value(state, i + 1, m1)
        state['output'].append(val)
        state['instruction_ptr'] = i + 2
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


def _run(state: dict) -> list:
    while not state['exit'] and not state['input_req']:
        state = _run_op(state)
    return state


def part1(values: list) -> int:
    state = {
        'values': list(values),
        'instruction_ptr': 0,
        'exit': False,
        'input_req': False,
        'input': [],
        'output': [],
        'relative_base': 0
    }
    out = _run(state)['output']
    return sum([ 1 if out[i] == 2 else 0 for i in range(2, len(out), 3) ])


def _pixel(n: int) -> str:
    return {
        0: ' ',
        1: '#',
        2: '*',
        3: '=',
        4: 'O'
    }[n]


def _screenshot(out: list) -> str:
    screen = ''
    for i in range(0, len(out), 3):
        if i > 0 and out[i] == 0:
            screen += '\n'
        tile = _pixel(out[i + 2])
        screen += tile
    system('clear')
    print(screen)


def _track_paddle(out: list, last_x: int) -> (int, int):
    o = [ t for t in [ out[i:i + 3] for i in range(0, len(out), 3) ] if t[2] == 3 ]
    if len(o) > 0:
        ball_x, ball_y, _ = o[0]
        return ball_x, ball_y
    return last_x, None


def _track_ball(out: list, last_x: int) -> (int, int):
    o = [ t for t in [ out[i:i + 3] for i in range(0, len(out), 3) ] if t[2] == 4 ]
    if len(o) > 0:
        ball_x, ball_y, _ = o[0]
        return ball_x, ball_y
    return last_x, None


def _refresh(out: list, diff: list) -> list:
    score = None
    for i in range(0, len(diff), 3):
        x, y, n = diff[i:i + 3]
        if x == -1 and y == 0:
            score = n
            continue
        out[3 * (37 * y + x) + 2] = n
    return score


def _joystick(ball: list, paddle: list) -> int:
    if ball[-1] > ball[-2]:
        return 1 if ball[-1] > paddle[-1] else 0
    elif ball[-1] == ball[-2]:
        return 1 if ball[-1] > paddle[-1] else 0 if ball[-1] == paddle[-1] else -1
    elif ball[-1] < ball[-2]:
        return 1 if ball[-1] > paddle[-1] else 0


def part2(values: list, display: bool=False) -> int:
    state = {
        'values': [ 2 ] + list(values)[1:],
        'instruction_ptr': 0,
        'exit': False,
        'input_req': False,
        'input': [],
        'output': [],
        'relative_base': 0
    }
    score = 0
    state = _run(state)
    screen = state['output']
    if display:
        _screenshot(screen)
    state['output'] = []
    ball = [_track_ball(screen, 0)[0] ]
    paddle = [ _track_paddle(screen, 0)[0] ]
    while not state['exit']:
        if display:
            sleep(0.001)
        ball.append(_track_ball(screen, ball[-1])[0])
        paddle.append(_track_paddle(screen, paddle[-1])[0])
        if state['input_req']:
            state['input_req'] = False
            state['input'].append(_joystick(ball, paddle))
        state = _run_op(state)
        if len(state['output']) % 3 == 0:
            s = _refresh(screen, state['output'])
            if s is not None:
                score = s
            if display:
                _screenshot(screen)
            state['output'] = []
        if display:
            print('Score:', score)
    return score


if __name__ == '__main__':
    with open('input.txt') as f:
        values = list(map(int, f.read().split(',')))
    print(part1(values))  # 286
    print(part2(values))  # 14538
