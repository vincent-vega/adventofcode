#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re


def _exe(registers: dict, C: int, value: int) -> dict:
    registers = dict(registers)
    registers[C] = value
    return registers


def _addr(registers: dict, A: int, B: int, C: int) -> dict:
    return _exe(registers, C, registers[A] + registers[B])


def _addi(registers: dict, A: int, B: int, C: int) -> dict:
    return _exe(registers, C, registers[A] + B)


def _mulr(registers: dict, A: int, B: int, C: int) -> dict:
    return _exe(registers, C, registers[A] * registers[B])


def _muli(registers: dict, A: int, B: int, C: int) -> dict:
    return _exe(registers, C, registers[A] * B)


def _banr(registers: dict, A: int, B: int, C: int) -> dict:
    return _exe(registers, C, registers[A] & registers[B])


def _bani(registers: dict, A: int, B: int, C: int) -> dict:
    return _exe(registers, C, registers[A] & B)


def _borr(registers: dict, A: int, B: int, C: int) -> dict:
    return _exe(registers, C, registers[A] | registers[B])


def _bori(registers: dict, A: int, B: int, C: int) -> dict:
    return _exe(registers, C, registers[A] | B)


def _setr(registers: dict, A: int, B: int, C: int) -> dict:
    return _exe(registers, C, registers[A])


def _seti(registers: dict, A: int, B: int, C: int) -> dict:
    return _exe(registers, C, A)


def _gtir(registers: dict, A: int, B: int, C: int) -> dict:
    return _exe(registers, C, 1 if A > registers[B] else 0)


def _gtri(registers: dict, A: int, B: int, C: int) -> dict:
    return _exe(registers, C, 1 if registers[A] > B else 0)


def _gtrr(registers: dict, A: int, B: int, C: int) -> dict:
    return _exe(registers, C, 1 if registers[A] > registers[B] else 0)


def _eqir(registers: dict, A: int, B: int, C: int) -> dict:
    return _exe(registers, C, 1 if A == registers[B] else 0)


def _eqri(registers: dict, A: int, B: int, C: int) -> dict:
    return _exe(registers, C, 1 if registers[A] == B else 0)


def _eqrr(registers: dict, A: int, B: int, C: int) -> dict:
    return _exe(registers, C, 1 if registers[A] == registers[B] else 0)


def _count_match(before: dict, instruction: tuple, after: dict) -> int:
    operations = [ _addr, _addi, _mulr, _muli, _banr, _bani, _borr, _bori, _setr, _seti, _gtir, _gtri, _gtrr, _eqir, _eqri, _eqrr ]
    _, *param = instruction
    return sum(1 for o in operations if o(before, *param) == after)


def part1(manual: list) -> int:
    return sum(1 for count in (_count_match(*page) for page in manual) if count > 2)


def _codes_map(manual: list) -> dict:
    mapping = {}
    operations = [ _addr, _addi, _mulr, _muli, _banr, _bani, _borr, _bori, _setr, _seti, _gtir, _gtri, _gtrr, _eqir, _eqri, _eqrr ]
    while operations:
        missing = len(operations)
        for page in manual:
            before, instruction, after = page
            code, *param = instruction
            if code in mapping:
                continue
            operation = None
            for o in operations:
                if o(before, *param) == after:
                    if operation is None:
                        operation = (code, o)
                    else:
                        # multiple match
                        operation = None
                        break
            if operation is not None:
                code, op = operation
                mapping[code] = op
                operations.remove(op)
        assert len(operations) < missing, 'Unable to map any new operation'
    return mapping


def part2(manual: list, test: str) -> int:
    mapping = _codes_map(manual)
    registers = { n: 0 for n in range(4) }
    for instruction in map(lambda x: _numbers(x), test.strip().split('\n')):
        code, *param = instruction
        registers = mapping[code](registers, *param)
    return registers[0]


def _numbers(string: str) -> tuple:
    return tuple(map(int, re.findall(r'-?\d+', string)))


def _parse(page: str) -> tuple:
    before, instruction, after = map(_numbers, page.split('\n'))
    return ({ r: n for r, n in enumerate(before) }, instruction, { r: n for r, n in enumerate(after) })


if __name__ == '__main__':
    with open('input.txt') as f:
        manual, test = f.read().split('\n\n\n')
        manual = [ _parse(page) for page in manual.split('\n\n') ]
    print(part1(manual))  # 607
    print(part2(manual, test))  # 577
