#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter, namedtuple
import re

Program = namedtuple('Program', [ 'name', 'weight', 'subtower' ])


def _parse(line: str) -> Program:
    chunks = [ x for x in re.split(' \(|\) -> |, |\)', line) if x != '' ]
    return Program(chunks[0], int(chunks[1]), set(chunks[2:]))


def _root(programs: list) -> str:
    for i in range(len(programs)):
        p = programs[i]
        if len(p.subtower) > 0 and len([ ii for ii in range(len(programs)) if ii != i and p.name in programs[ii].subtower ]) == 0:
            return p.name
    raise Exception('Not found')


def _weight_tower(programs: dict, name: str) -> int:
    return programs[name].weight + sum([ _weight_tower(programs, p) for p in programs[name].subtower ])


def _balance(programs: dict, name: str, weight: int=None) -> int:
    w = [ (s, _weight_tower(programs, s)) for s in programs[name].subtower ]
    c = Counter([ v for _, v in w ])
    if len(c) == 1:
        if weight is None:
            raise Exception('Already balanced')
        return weight - sum([ v for _, v in w ])
    elif len(c) > 2:
        raise Exception('Too many unbalanced sub-towers')
    unbalanced_weight, _ = min(c.items(), key=lambda x: x[1])
    expected_weight, __  = max(c.items(), key=lambda x: x[1])
    unbalanced_name = [ k for k, v in w if v == unbalanced_weight ][0]
    return _balance(programs, unbalanced_name, expected_weight)


def part1(programs: dict) -> str:
    return _root(list(programs.values()))


def part2(programs: dict) -> int:
    return _balance(programs, _root(list(programs.values())))


if __name__ == '__main__':
    with open('input.txt') as f:
        programs = { p.name: p for p in map(_parse, f.read().splitlines()) }
    print(part1(programs))  # cqmvs
    print(part2(programs))  # 2310
