#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import namedtuple
from math import sqrt

Instruction = namedtuple('Instruction', [ 'cmd', 'src', 'dst' ])


def _load(mem: dict, dst: str) -> int:
    return mem[dst] if dst in mem else int(dst)


def _exec(mem: dict, i: Instruction) -> int:
    if i.cmd == 'set':
        mem[i.src] = _load(mem, i.dst)
    elif i.cmd == 'sub':
        mem[i.src] -= _load(mem, i.dst)
    elif i.cmd == 'mul':
        mem[i.src] *= _load(mem, i.dst)
    elif i.cmd == 'jnz' and _load(mem, i.src) != 0:
        return int(i.dst)
    return 1


def part1(program: list) -> int:
    ptr = cnt = 0
    mem = { chr(n + ord('a')): 0 for n in range(ord('h') + 1 - ord('a')) }
    while ptr > -1 and ptr < len(program):
        if program[ptr].cmd == 'mul':
            cnt += 1
        ptr += _exec(mem, program[ptr])
    return cnt


def part2() -> int:
    # see code analysis "solution-notes.txt"
    prime_num_cnt = 0
    for b in range(108417, 125401, 34):
        for d in range(3, int(sqrt(b)), 2):
            if b % d == 0:
                break
        else:
            prime_num_cnt += 1
    return (125400 - 108400) // 17 + 1 - prime_num_cnt  # non-prime numbers count between 108400 and 125400


if __name__ == '__main__':
    with open('input.txt') as f:
        program = [ Instruction(*l.split()) for l in f.read().splitlines() ]
    print(part1(program))  # 6724
    print(part2())  # 903
