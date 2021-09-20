#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict, namedtuple
import re

Actions = namedtuple('Actions', [ 'write', 'move', 'next' ])


def _resize(tape: list, beginning: bool, size: int) -> list:
    return [ 0 ] * size + tape if beginning else tape + [ 0 ] * size


def part1(blueprint: dict) -> int:
    cur_state = 'A'
    tape = [ 0 ] * 1024
    ptr = len(tape) // 2
    resize_N = 8 * 2**10
    for _ in range(blueprint['steps']):
        action = blueprint[cur_state][tape[ptr]]
        tape[ptr] = action.write
        if ptr == 0 and action.move < 0:
            tape = _resize(tape, True, resize_N)
            ptr = resize_N
            resize_N *= 2
        elif ptr == len(tape) - 1 and action.move > 0:
            tape = _resize(tape, False, resize_N)
            resize_N *= 2
        ptr += action.move
        cur_state = action.next
    return sum(tape)


def _parse(lines: list) -> dict:
    blueprint = defaultdict(dict)
    cur_state = cur_val = cur_write_val = cur_offset = None
    for l in lines:
        if 'checksum' in l:
            blueprint['steps'] = int(re.findall('\\d+', l).pop())
        elif 'In state' in l:
            cur_state = l.split()[-1][:-1]
        elif 'If the current value is' in l:
            cur_val = int(re.findall('\\d+', l).pop())
        elif 'Write the value' in l:
            cur_write_val = int(re.findall('\\d+', l).pop())
        elif 'Move one slot to' in l:
            cur_offset = 1 if l.endswith('right.') else -1
        elif 'Continue with state' in l:
            blueprint[cur_state][cur_val] = Actions(cur_write_val, cur_offset, l.split()[-1][:-1])
    return blueprint


if __name__ == '__main__':
    with open('input.txt') as f:
        blueprint = _parse(f.read().splitlines())
    print(part1(blueprint))  # 4217
