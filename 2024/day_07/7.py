#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import product
import re


def _verified(result: int, numbers: list[int], operators: list[str]) -> bool:
    r = numbers[0]
    for idx, n in enumerate(numbers[1:]):
        match operators[idx]:
            case '+':
                r += n
            case '*':
                r = r * n
            case '||':
                r = int(str(r) + str(n))
        if r > result:
            return False
    return r == result


def _calibrated(result: int, numbers: list[int], with_concat: bool = False) -> bool:
    operators = [ '+', '*', '||' ] if with_concat else [ '+', '*' ]
    for o in product(operators, repeat=len(numbers) - 1):
        if _verified(result, numbers, o):
            return True
    return False


def part1(equations: list[tuple[int]]) -> int:
    return sum(result for result, *numbers in equations if _calibrated(result, numbers))


def part2(equations: list[tuple[int]]) -> int:
    return sum(result for result, *numbers in equations if _calibrated(result, numbers, True))


if __name__ == '__main__':
    with open('input.txt') as f:
        equations = [ tuple(map(int, re.findall(r'-?\d+', line))) for line in f.read().splitlines() ]
    print(part1(equations))  # 6392012777720
    print(part2(equations))  # 61561126043536
