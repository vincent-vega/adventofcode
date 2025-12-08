#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from functools import reduce


def part1(lines: list[str]) -> int:
    problems = defaultdict(list)
    for line in lines:
        for col, c in enumerate(line.split()):
            problems[col].append(c if c in {'+', '*'} else int(c))
    return sum(_evaluate(v) for v in problems.values())


def part2(lines: list[str]) -> int:
    problems = defaultdict(list)
    col = 0
    for idx in range(len(lines[0])):
        values = [ line[idx] for line in lines ]
        if values[-1] != ' ':
            operation = values[-1]
        if not all(v == ' ' for v in values):
            problems[col].append(int(''.join(values[:-1])))
            if idx != len(lines[0]) - 1:
                continue
        problems[col].append(operation)
        operation = None
        col += 1
    return sum(_evaluate(v) for v in problems.values())


def _evaluate(elements: list) -> int:
    return sum(elements[:-1]) if elements[-1] == '+' else reduce(lambda a, b: a * b, elements[:-1])


if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.read().splitlines()
    print(part1(lines))  # 5552221122013
    print(part2(lines))  # 11371597126232
