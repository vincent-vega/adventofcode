#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import namedtuple

Sloc = namedtuple('Sloc', [ 'instr', 'value' ])


class LoopException(Exception):
    pass


def _patch(code: list, idx: int) -> list:
    return [ code[i] if i != idx else Sloc('jmp' if code[i].instr == 'nop' else 'nop', code[i].value) for i in range(len(code)) ]


def _run(code: list) -> int:
    seen = set()
    ptr, acc = 0, 0
    while ptr not in seen:
        seen.add(ptr)
        sloc = code[ptr]
        ptr += sloc.value if sloc.instr == 'jmp' else 1
        if sloc.instr == 'acc':
            acc += sloc.value
        if ptr == len(code):
            return acc
    raise LoopException(acc)


def part2(code: list) -> int:
    for i in filter(lambda x: code[x].instr in { 'nop', 'jmp' }, range(len(code))):
        try:
            return _run(_patch(code, i))
        except LoopException as e:
            pass
    raise Exception('Not found')


def part1(code: list) -> int:
    try:
        _run(code)
    except LoopException as e:
        return int(str(e))
    raise Exception('Not found')


if __name__ == '__main__':
    with open('input.txt') as f:
        code = [ Sloc(instr, int(val)) for instr, val in map(lambda l: l.split(), f.read().splitlines()) ]
    print(part1(code))  # 2051
    print(part2(code))  # 2304
