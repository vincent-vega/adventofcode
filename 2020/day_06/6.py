#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce


def part1(forms: list) -> int:
    return sum([ len(reduce(lambda x, y: x | y, group)) for group in forms ])


def part2(forms: list) -> int:
    return sum([ len(reduce(lambda x, y: x & y, group)) for group in forms ])


if __name__ == '__main__':
    with open('input.txt') as f:
        forms = [ list(map(set, group.split('\n'))) for group in f.read().split('\n\n') ]
    print(part1(forms))  # 7283
    print(part2(forms))  # 3520
