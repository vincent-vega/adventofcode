#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.lib import _print
from dataclasses import dataclass
import re


@dataclass
class Computer:
    A: int
    B: int
    C: int


def _combo(computer: Computer, operand: int) -> int:
    match operand:
        case 0 | 1 | 2 | 3:
            return operand
        case 4:
            return computer.A
        case 5:
            return computer.B
        case 6:
            return computer.C
        case _:
            raise Exception(f'Unknown operand {operand}')


def _run(computer: Computer, program: list[int]) -> str:
    ip = 0
    out = []
    while ip < len(program):
        match opcode := program[ip]:
            case 0:
                computer.A = computer.A // 2 ** _combo(computer, program[ip + 1])
            case 1:
                computer.B = computer.B ^ program[ip + 1]
            case 2:
                computer.B = _combo(computer, program[ip + 1]) % 8
            case 3:
                if computer.A != 0:
                    ip = program[ip + 1]
            case 4:
                computer.B = computer.B ^ computer.C
            case 5:
                out.append(_combo(computer, program[ip + 1]) % 8)
            case 6:
                computer.B = computer.A // 2 ** _combo(computer, program[ip + 1])
            case 7:
                computer.C = computer.A // 2 ** _combo(computer, program[ip + 1])
            case _:
                raise Exception(f'Unknown opcode {opcode}')
        if opcode != 3 or computer.A == 0:
            ip += 2
    return out


def part1(computer: Computer, program: list[int]) -> str:
    return ','.join(map(str, _run(computer, program)))


def part2(program: list[int]) -> int:
    pass


if __name__ == '__main__':
    with open('input.txt') as f:
        A, B, C, *program = map(int, re.findall(r'\d+', f.read()))
    print(part1(Computer(A, B, C), program))  # 5,1,3,4,3,7,2,1,7
    _print(part2(program))  #
