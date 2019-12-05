#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def _run_op(values, instruction_ptr, sys_id):
    POSITION_MODE = 0
    instruction = values[instruction_ptr]
    def _get_param_value(v, i, m):
        return v[v[i%len(v)]%len(v)] if m == POSITION_MODE else v[i]
    def _add(v, i, m1, m2):
        v1 = _get_param_value(v, i + 1, m1)
        v2 = _get_param_value(v, i + 2, m2)
        v[v[i + 3]%len(v)] = v1 + v2
        return i + 4
    def _mul(v, i, m1, m2):
        v1 = _get_param_value(v, i + 1, m1)
        v2 = _get_param_value(v, i + 2, m2)
        v[v[i + 3]%len(v)] = v1*v2
        return i + 4
    def _set(v, i, _, __):
        v[v[i + 1]%len(v)] = sys_id
        return i + 2
    def _out(v, i, m1, _):
        v = _get_param_value(v, i + 1, m1)
        if v != 0:
            print(v)
        return i + 2 if v == 0 else None
    def _jump_true(v, i, m1, m2):
        v1 = _get_param_value(v, i + 1, m1)
        v2 = _get_param_value(v, i + 2, m2)
        return v2 if v1 != 0 else i + 3
    def _jump_false(v, i, m1, m2):
        v1 = _get_param_value(v, i + 1, m1)
        v2 = _get_param_value(v, i + 2, m2)
        return v2 if v1 == 0 else i + 3
    def _less_than(v, i, m1, m2):
        v1 = _get_param_value(v, i + 1, m1)
        v2 = _get_param_value(v, i + 2, m2)
        v[v[i + 3]%len(v)] = 1 if v1 < v2 else 0
        return i + 4
    def _equals(v, i, m1, m2):
        v1 = _get_param_value(v, i + 1, m1)
        v2 = _get_param_value(v, i + 2, m2)
        v[v[i + 3]%len(v)] = 1 if v1 == v2 else 0
        return i + 4
    def _exit(*argv):
        return None
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

def _run_prog(values, sys_id):
    idx = 0
    while idx != None:
        idx = _run_op(values, idx, sys_id)

def part1(values, sys_id):
    return _run_prog(values, sys_id)

def part2(values, sys_id):
    return _run_prog(values, sys_id)

if __name__ == '__main__':
    with open('input.txt') as f:
        values = list(map(int, f.read().split(',')))
    part1(list(values), 1) # 13087969
    part2(values, 5) # 14110739

