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

    @staticmethod
    def _get_param_value(p: list, i: int, m: int) -> int:
        return p[p[i % len(p)] % len(p)] if m == Intcode.POSITION_MODE else p[i]

    @staticmethod
    def _add(state: Intcode_State, i: int, m1: int, m2: int):
        p = state.program
        v1 = Intcode._get_param_value(p, i + 1, m1)
        v2 = Intcode._get_param_value(p, i + 2, m2)
        p[p[i + 3] % len(p)] = v1 + v2
        state.instruction_ptr = i + 4

    @staticmethod
    def _mul(state: Intcode_State, i: int, m1: int, m2: int):
        p = state.program
        v1 = Intcode._get_param_value(p, i + 1, m1)
        v2 = Intcode._get_param_value(p, i + 2, m2)
        p[p[i + 3] % len(p)] = v1 * v2
        state.instruction_ptr = i + 4

    @staticmethod
    def _set(state: Intcode_State, i: int, _, __):
        p = state.program
        if len(state.input) == 0:
            state.input_req = True
        else:
            state.input_req = False
            p[p[i + 1] % len(p)] = state.input.popleft()
            state.instruction_ptr = i + 2

    @staticmethod
    def _out(state: Intcode_State, i: int, m1: int, _):
        state.instruction_ptr = i + 2
        state.output.append(Intcode._get_param_value(state.program, i + 1, m1))

    @staticmethod
    def _jump_true(state: Intcode_State, i: int, m1: int, m2: int):
        v1 = Intcode._get_param_value(state.program, i + 1, m1)
        v2 = Intcode._get_param_value(state.program, i + 2, m2)
        state.instruction_ptr = v2 if v1 != 0 else i + 3

    @staticmethod
    def _jump_false(state: Intcode_State, i: int, m1: int, m2: int):
        v1 = Intcode._get_param_value(state.program, i + 1, m1)
        v2 = Intcode._get_param_value(state.program, i + 2, m2)
        state.instruction_ptr = v2 if v1 == 0 else i + 3

    @staticmethod
    def _less_than(state: Intcode_State, i: int, m1: int, m2: int):
        p = state.program
        v1 = Intcode._get_param_value(p, i + 1, m1)
        v2 = Intcode._get_param_value(p, i + 2, m2)
        p[p[i + 3] % len(p)] = 1 if v1 < v2 else 0
        state.instruction_ptr = i + 4

    @staticmethod
    def _equals(state: Intcode_State, i: int, m1: int, m2: int):
        p = state.program
        v1 = Intcode._get_param_value(p, i + 1, m1)
        v2 = Intcode._get_param_value(p, i + 2, m2)
        p[p[i + 3] % len(p)] = 1 if v1 == v2 else 0
        state.instruction_ptr = i + 4

    @staticmethod
    def _exit(state: Intcode_State, *argv):
        state.exit = True

    @staticmethod
    def _get_opcode(instr: int) -> int:
        return instr % 100

    @staticmethod
    def _get_mode(instr: int) -> (int, int):
        return instr // 100 % 10, instr // 1000

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
            99: Intcode._exit
        }[Intcode._get_opcode(instruction)](state, instruction_ptr, *Intcode._get_mode(instruction))
