#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import namedtuple
import re

Instruction = namedtuple('Instruction', [ 'register', 'op', 'val', 'par1', 'cond', 'par2' ])


def _parse(line: str) -> Instruction:
    chunks = [ x for x in re.split(' if | ', line) if x != '' ]
    return Instruction(chunks[0], chunks[1], int(chunks[2]), chunks[3], chunks[4], int(chunks[5]))


def _check(reg: str, cond: str, val: int) -> bool:
    if cond == '==':
        return reg == val
    elif cond == '!=':
        return reg != val
    elif cond == '<':
        return reg < val
    elif cond == '<=':
        return reg <= val
    elif cond == '>':
        return reg > val
    elif cond == '>=':
        return reg >= val


def _run(instructions: list) -> (int, int):
    CPU = {}
    M = None
    for i in instructions:
        if _check(CPU.get(i.par1, 0), i.cond, i.par2):
             v = CPU.get(i.register, 0) + (1 if i.op == 'inc' else -1) * i.val
             if M is None or M < v:
                M = v
             CPU[i.register] = v
    return max(CPU.values()), M


def part1(instructions: list) -> int:
    v, _ = _run(instructions)
    return v


def part2(instructions: list) -> int:
    _, v = _run(instructions)
    return v


if __name__ == '__main__':
    with open('input.txt') as f:
        instructions = [ _parse(l) for l in f.read().splitlines() ]
    print(part1(instructions))  # 4448
    print(part2(instructions))  # 6582
