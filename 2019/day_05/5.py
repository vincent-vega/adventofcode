#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from intcode import run_op


def _run_prog(values, sys_id):
    idx = 0
    while idx is not None:
        idx = run_op(values, idx, sys_id)


def part1(values, sys_id):
    return _run_prog(values, sys_id)


def part2(values, sys_id):
    return _run_prog(values, sys_id)


if __name__ == '__main__':
    with open('input.txt') as f:
        values = list(map(int, f.read().split(',')))
    part1(list(values), 1)  # 13087969
    part2(values, 5)  # 14110739
