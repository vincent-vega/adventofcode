#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict, namedtuple
import re

Actions = namedtuple('Actions', [ 'write', 'move', 'next' ])


def part1(blueprint: dict) -> int:
    cur_state = blueprint['start_state']
    assert cur_state in blueprint, 'Unknown start state'
    tape = {}
    ptr = 0
    for _ in range(blueprint['steps']):
        action = blueprint[cur_state][tape.get(ptr, 0)]
        tape[ptr] = action.write
        ptr += action.move
        cur_state = action.next
    return sum(tape.values())


def _parse(lines: list) -> dict:
    blueprint = defaultdict(dict)
    cur_state = cur_val = cur_write_val = cur_offset = None
    for l in lines:
        if 'Begin in state' in l:
            blueprint['start_state'] = l.split()[-1][:-1]
        elif 'checksum' in l:
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
