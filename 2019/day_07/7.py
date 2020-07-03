#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from intcode import Intcode, Intcode_State
from itertools import permutations


def _run_phase_feedback(phase_list: list, values: list) -> int:
    states = [ Intcode_State(values, [ phase ]) for phase in phase_list ]
    state_idx = 0
    states[state_idx].input.append(0)
    while not states[state_idx].exit:
        Intcode.run(states[state_idx])
        if states[state_idx].output:
            out = states[state_idx].output.pop()
            state_idx = (state_idx + 1) % len(states)
            states[state_idx].input.append(out)
    return out


def _run_phase(phase_list: list, values: list) -> int:
    out = 0
    for phase in phase_list:
        state = Intcode_State(values, [ phase, out ])
        while not state.exit:
            Intcode.run(state)
        out = state.output.pop()
    return out


def part1(values: list) -> int:
    return max([ _run_phase(p, values) for p in permutations(range(5)) ])


def part2(values: list) -> int:
    return max([ _run_phase_feedback(p, values) for p in permutations(range(5, 10)) ])


if __name__ == '__main__':
    with open('input.txt') as f:
        values = list(map(int, f.read().split(',')))
    print(part1(values))  # 262086
    print(part2(values))  # 5371621
