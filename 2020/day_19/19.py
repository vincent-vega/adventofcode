#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce
from typing import Union
import re


def _dependencies(what: str) -> Union[list, str]:
    if re.match('"[a-z]"', what):
        return what.replace('"', '')
    return list(map(lambda x: [ int(n) for n in x.split() ], [ w for w in what.split(" | ") ]))


def _flat(nested_list: list) -> list:
    result = set()
    for l in nested_list:
        if type(l) is list:
            result.update(list(_flat(l)))
        else:
            result.add(l)
    return list(result)


def _expand(rules: dict) -> dict:
    def _merge(a, b):
        if len(a) == len(b) == 1:
            return a[0] + b[0]
        r = []
        for i in range(len(a)):
            for j in range(len(b)):
                assert type(a[i] + b[j]) is str
                r.append(a[i] + b[j])
        return r

    expanded = {}
    remaining = rules.keys() - expanded.keys()
    while len(remaining) > 0:
        for n in remaining:
            if type(rules[n]) is str:
                expanded[n] = [ rules[n] ]
            elif reduce(lambda x, y: x & y, [ ll in expanded for l in rules[n] for ll in l ]):
                expanded[n] = _flat([ reduce(_merge, [ expanded[rr] for rr in r ]) for r in rules[n] ])
        remaining = rules.keys() - expanded.keys()
    return expanded


def part1(valid: set, messages: list) -> int:
    return len([ m for m in messages if m in valid ])


if __name__ == '__main__':
    with open('input.txt') as f:
        rules, messages = f.read().split('\n\n')
        rules = { int(n): _dependencies(w.strip()) for n, w in map(lambda x: x.split(':'), [ r for r in rules.split('\n') ]) }
        messages = messages.split('\n')
    expanded = _expand(rules)
    print(part1(set(expanded[0]), messages))
