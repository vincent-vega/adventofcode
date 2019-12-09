#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import permutations

def _run_op(state: dict, input_values: list) -> dict:
    POSITION_MODE = 0
    instruction_ptr = state['instruction_ptr']
    values = state['values']
    instruction = values[instruction_ptr]
    def _get_param_value(v, i, m):
        return v[v[i%len(v)]%len(v)] if m == POSITION_MODE else v[i]
    def _add(v, i, m1, m2):
        v1 = _get_param_value(v, i + 1, m1)
        v2 = _get_param_value(v, i + 2, m2)
        v[v[i + 3]%len(v)] = v1 + v2
        state['instruction_ptr'] = i + 4
        return state
    def _mul(v, i, m1, m2):
        v1 = _get_param_value(v, i + 1, m1)
        v2 = _get_param_value(v, i + 2, m2)
        v[v[i + 3]%len(v)] = v1*v2
        state['instruction_ptr'] = i + 4
        return state
    def _set(v, i, _, __):
        v[v[i + 1]%len(v)] = input_values.pop()
        state['instruction_ptr'] = i + 2
        return state
    def _out(v, i, m1, _):
        state['instruction_ptr'] = i + 2
        state['output'] = _get_param_value(v, i + 1, m1)
        return state
    def _jump_true(v, i, m1, m2):
        v1 = _get_param_value(v, i + 1, m1)
        v2 = _get_param_value(v, i + 2, m2)
        state['instruction_ptr'] = v2 if v1 != 0 else i + 3
        return state
    def _jump_false(v, i, m1, m2):
        v1 = _get_param_value(v, i + 1, m1)
        v2 = _get_param_value(v, i + 2, m2)
        state['instruction_ptr'] = v2 if v1 == 0 else i + 3
        return state
    def _less_than(v, i, m1, m2):
        v1 = _get_param_value(v, i + 1, m1)
        v2 = _get_param_value(v, i + 2, m2)
        v[v[i + 3]%len(v)] = 1 if v1 < v2 else 0
        state['instruction_ptr'] = i + 4
        return state
    def _equals(v, i, m1, m2):
        v1 = _get_param_value(v, i + 1, m1)
        v2 = _get_param_value(v, i + 2, m2)
        v[v[i + 3]%len(v)] = 1 if v1 == v2 else 0
        state['instruction_ptr'] = i + 4
        return state
    def _exit(*argv):
        state['exit'] = True
        return state
    def _get_opcode(instr):
        return instr%100
    def _get_mode(instr):
        return instr//100%10, instr//1000
    return {
        1:  _add,
        2:  _mul,
        3:  _set,
        4:  _out,
        5:  _jump_true,
        6:  _jump_false,
        7:  _less_than,
        8:  _equals,
        99: _exit
    }[_get_opcode(instruction)](values, instruction_ptr, *_get_mode(instruction))

def _run_prog(amp_state: dict, params: list) -> dict:
    amp_state['output'] = None
    while not amp_state['exit'] and amp_state['output'] is None:
        amp_state = _run_op(amp_state, params)
    return amp_state

def _run_phase_feedback(phase_list: list, values: list) -> int:
    out_val = 0
    amp_states = [ { 'values': list(values), 'instruction_ptr': 0, 'exit': False, 'output': None} for _ in range(len(phase_list)) ]
    for i in range(len(phase_list)):
        state = _run_prog(amp_states[i], [ out_val, phase_list[i] ])
        out_val = state['output']
    i = 0
    while not state['exit']:
        state = _run_prog(amp_states[i%len(phase_list)], [ out_val ])
        if state['output'] is not None:
            out_val = state['output']
        i += 1
    return out_val

def _run_phase(phase_list: list, values: list) -> int:
    out_val = 0
    amp_states = [ { 'values': list(values), 'instruction_ptr': 0, 'exit': False, 'output': None } for _ in range(len(phase_list)) ]
    for i in range(len(phase_list)):
        state = _run_prog(amp_states[i], [ out_val, phase_list[i] ])
        if state['output'] is not None:
            out_val = state['output']
    return out_val

def part1(values: list) -> int:
    return max([ _run_phase(p, values) for p in permutations(range(5)) ])

def part2(values: list) -> int:
    return max([ _run_phase_feedback(p, values) for p in permutations(range(5, 10)) ])

if __name__ == '__main__':
    with open('input.txt') as f:
        values = list(map(int, f.read().split(',')))
    print(part1(values)) # 262086
    print(part2(values)) # 5371621

