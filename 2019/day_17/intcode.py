#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque


class Intcode_State:

    def __init__(self, program: list, input_values: list=None):
        self.program = list(program)
        self.instruction_ptr = 0
        self.exit = False
        self.output = deque()
        self.input = deque([] if input_values is None else list(input_values))
        self.input_req = False
        self.relative_base = 0

    def __repr__(self):
        return f'> exit: {self.exit}\n> output: {self.output}\n> input_req: {self.input_req}\n> input: {self.input}'


class Intcode:
    POSITION_MODE = 0
    IMMEDIATE_MODE = 1
    RELATIVE_MODE = 2

    @staticmethod
    def _resize(mem: list, num: int):
        mem.extend([ 0 for _ in range(num) ])

    @staticmethod
    def _check_resize(mem: list, addr: int):
        if addr > len(mem) - 1:
            Intcode._resize(mem, addr - len(mem) + 1)

    @staticmethod
    def _read_value(state: Intcode_State, i: int, m: int):
        p = state.program
        base = state.relative_base
        if m == Intcode.IMMEDIATE_MODE:
            return p[i]
        addr = p[i] if m == Intcode.POSITION_MODE else base + p[i]
        Intcode._check_resize(p, addr)
        return p[addr]

    @staticmethod
    def _write_value(state: Intcode_State, i: int, value: int, m: int):
        p = state.program
        base = state.relative_base
        assert m == Intcode.POSITION_MODE or m == Intcode.RELATIVE_MODE
        addr = p[i] if m == Intcode.POSITION_MODE else base + p[i]
        Intcode._check_resize(p, addr)
        p[addr] = value

    @staticmethod
    def _add(state: Intcode_State, i: int, m1: int, m2: int, m3: int):
        v1 = Intcode._read_value(state, i + 1, m1)
        v2 = Intcode._read_value(state, i + 2, m2)
        Intcode._write_value(state, i + 3, v1 + v2, m3)
        state.instruction_ptr = i + 4

    @staticmethod
    def _mul(state: Intcode_State, i: int, m1: int, m2: int, m3: int):
        v1 = Intcode._read_value(state, i + 1, m1)
        v2 = Intcode._read_value(state, i + 2, m2)
        Intcode._write_value(state, i + 3, v1 * v2, m3)
        state.instruction_ptr = i + 4

    @staticmethod
    def _set(state: Intcode_State, i: int, m1: int, _, __):
        if len(state.input) == 0:
            state.input_req = True
        else:
            state.input_req = False
            Intcode._write_value(state, i + 1, state.input.popleft(), m1)
            state.instruction_ptr = i + 2

    @staticmethod
    def _out(state: Intcode_State, i: int, m1: int, _, __):
        val = Intcode._read_value(state, i + 1, m1)
        state.output.append(val)
        state.instruction_ptr = i + 2

    @staticmethod
    def _jump_true(state: Intcode_State, i: int, m1: int, m2: int, _):
        v1 = Intcode._read_value(state, i + 1, m1)
        v2 = Intcode._read_value(state, i + 2, m2)
        state.instruction_ptr = v2 if v1 != 0 else i + 3

    @staticmethod
    def _jump_false(state: Intcode_State, i: int, m1: int, m2: int, _):
        v1 = Intcode._read_value(state, i + 1, m1)
        v2 = Intcode._read_value(state, i + 2, m2)
        state.instruction_ptr = v2 if v1 == 0 else i + 3

    @staticmethod
    def _less_than(state: Intcode_State, i: int, m1: int, m2: int, m3: int):
        v1 = Intcode._read_value(state, i + 1, m1)
        v2 = Intcode._read_value(state, i + 2, m2)
        Intcode._write_value(state, i + 3, 1 if v1 < v2 else 0, m3)
        state.instruction_ptr = i + 4

    @staticmethod
    def _equals(state: Intcode_State, i: int, m1: int, m2: int, m3: int):
        v1 = Intcode._read_value(state, i + 1, m1)
        v2 = Intcode._read_value(state, i + 2, m2)
        Intcode._write_value(state, i + 3, 1 if v1 == v2 else 0, m3)
        state.instruction_ptr = i + 4

    @staticmethod
    def _adjust_base(state: Intcode_State, i: int, m1: int, _, __):
        state.relative_base += Intcode._read_value(state, i + 1, m1)
        state.instruction_ptr = i + 2

    @staticmethod
    def _exit(state: Intcode_State, *argv):
        state.exit = True

    @staticmethod
    def _get_opcode(instr: int) -> int:
        return instr % 100

    @staticmethod
    def _get_mode(instr: int) -> (int, int, int):
        return instr // 100 % 10, instr // 1000 % 10, instr // 10000

    @staticmethod
    def run(state: Intcode_State):
        instruction_ptr = state.instruction_ptr
        program = state.program
        instruction = program[instruction_ptr]
        {
            1: Intcode._add,
            2: Intcode._mul,
            3: Intcode._set,
            4: Intcode._out,
            5: Intcode._jump_true,
            6: Intcode._jump_false,
            7: Intcode._less_than,
            8: Intcode._equals,
            9: Intcode._adjust_base,
            99: Intcode._exit
        }[Intcode._get_opcode(instruction)](state, instruction_ptr, *Intcode._get_mode(instruction))
