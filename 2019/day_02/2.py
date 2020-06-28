#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import product


def _run_op(values, instruction_pointer):
    values[values[instruction_pointer + 3]] = {
        1: values[values[instruction_pointer + 1]] + values[values[instruction_pointer + 2]],
        2: values[values[instruction_pointer + 1]] * values[values[instruction_pointer + 2]]
    }.get(values[instruction_pointer])


def _init(values, noun, verb):
    values[1] = noun
    values[2] = verb


def _run_prog(values, noun, verb):
    _init(values, noun, verb)
    for i in range(0, len(values), 4):
        if values[i] == 99:
            break
        _run_op(values, i)
    return values[0]


def part1(values):
    return _run_prog(values, 12, 2)


def part2(values):
    for noun, verb in product(range(100), range(100)):
        if _run_prog(list(values), noun, verb) == 19690720:
            return 100 * noun + verb


if __name__ == '__main__':
    with open('input.txt') as f:
        values = list(map(int, f.read().split(',')))
    print(part1(list(values)))  # 6087827
    print(part2(values))  # 5379
