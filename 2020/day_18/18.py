#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce
from operator import mul, add
from typing import Callable
import re


def _match_parenth_idx(block: list) -> int:
    balance = 1
    for idx in range(1, len(block)):
        balance += 1 if block[idx] == '(' else -1 if block[idx] == ')' else 0
        if balance == 0:
            return idx
    return -1


def _calc2(block: list) -> int:
    while '+' in block:
        idx = block.index('+')
        ending = [] if len(block) == idx + 2 else block[idx + 2:]
        block = block[:idx - 1] + [ block[idx - 1] + block[idx + 1] ] + ending
    return reduce(mul, filter(lambda c: c != '*', block))


def _calc1(block: list) -> int:
    idx, result = 1, block[0]
    while idx < len(block):
        operator = {'+': add, '*': mul}[block[idx]]
        result = operator(result, block[idx + 1])
        idx += 2
    return result


def _solve(block: list, calc_f: Callable) -> int:
    while '(' in block:
        idx = block.index('(')
        end = idx + _match_parenth_idx(block[idx:])
        block = block[0:idx] + [ _solve(block[idx + 1:end], calc_f) ] + block[end + 1:]
    return calc_f(block)


def part1(expressions: list):
    return sum([ _solve(e, _calc1) for e in expressions ])


def part2(expressions: list):
    return sum([ _solve(e, _calc2) for e in expressions ])


if __name__ == '__main__':
    with open('input.txt') as f:
        expressions = [ list(map(lambda n: int(n) if re.match('-?\\d+', n) else n, line)) for line in map(lambda l: l.split(), f.read().replace('(', '( ').replace(')', ' )').splitlines()) ]
    print(part1(expressions))  # 45283905029161
    print(part2(expressions))  # 216975281211165
