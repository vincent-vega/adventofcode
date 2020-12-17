#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce
import re


def _satisfies(boundaries: list, value: int) -> bool:
    for min_v, max_v in boundaries:
        if value >= min_v and value <= max_v:
            return True
    return False


def _matched_rules(rules: dict, col_values: list) -> set:
    match = set()
    for name, boundaries in rules.items():
        for v in col_values:
            if not _satisfies(boundaries, v):
                break
        else:
            match.add(name)
    return match


def _clean(compatible: list, column: set) -> list:
    return [ (i, c - column) for i, c in compatible ]


def part1(invalid: list) -> int:
    return sum(invalid)


def part2(rules: dict, ticket: list, nearby: list) -> int:
    compatible = [ (i, _matched_rules(rules, [ n[i] for n in nearby ])) for i in range(len(ticket)) ]  # column idx, set of satisfied rules
    mapping = {}  # column name -> column idx
    while len(mapping.keys()) < len(ticket):
        for idx, name in filter(lambda v: len(v[1]) == 1, compatible):
            col_name = name.pop()
            mapping[col_name] = idx
            compatible = _clean([ (i, c) for i, c in compatible if i != idx ], set([ col_name ]))
            break
        else:
            raise Exception('Unable to find a solution')
    return reduce(lambda a, b: a * b, [ ticket[idx] for name, idx in mapping.items() if 'departure' in name ])


def _parse(rules: str) -> dict:
    def _boundaries(values) -> list:
        return [[ int(d) for d in re.findall('\\d+', delta) ] for delta in values.split(' or ') ]

    return { name: _boundaries(values) for name, values in map(lambda r: r.split(': '), rules.split('\n')) }


def _invalid(rules: str, nearby: list) -> list:
    valid = set()
    for r in rules.split('\n'):
        _, r = r.split(': ')
        for rr in r.split(' or '):
            m, M = list(map(int, rr.split('-')))
            valid.update(range(m, M + 1))
    return [ v for n in nearby for v in n if v not in valid ]


if __name__ == '__main__':
    with open('input.txt') as f:
        rules, ticket, nearby = [ x for x in f.read().split('\n\n') ]
    ticket = list(map(int, ticket[len('your ticket: '):].split(',')))
    nearby = [ list(map(int, o.split(','))) for o in nearby[len('nearby tickets: '):-1].split('\n') ]
    invalid = _invalid(rules, nearby)
    print(part1(invalid))  # 25961
    invalid = set(invalid)
    nearby = [ n for n in nearby if len(invalid & set(n)) == 0 ]
    print(part2(_parse(rules), ticket, nearby))  # 603409823791
