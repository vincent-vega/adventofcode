#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce
from itertools import product
from typing import Union, Pattern
import regex


def _dependencies(what: str) -> Union[list, str]:
    if regex.match('"[a-z]"', what):
        return what.replace('"', '')
    return list(map(lambda x: [ int(n) for n in x.split() ], [ w for w in what.split(" | ") ]))


def _expand(rules: dict) -> dict:
    def _merge(a: set, b: set) -> set:
        return { ''.join(p) for p in product(a, b) }

    expanded, remaining = {}, rules.keys()
    while remaining:
        for cur_rule in remaining:
            if type(rules[cur_rule]) is str:  # elementary rule
                expanded[cur_rule] = { rules[cur_rule] }
            elif all(nn in expanded for n in rules[cur_rule] for nn in n if nn != cur_rule):
                # cur_rule can be expanded: all the dependencies have been expanded already
                if cur_rule in { nn for n in rules[cur_rule] for nn in n }:
                    # rule with loop
                    dependencies = [ nn for n in rules[cur_rule] for nn in n if cur_rule not in n ]
                    chunks = { x for x in reduce(_merge, [ expanded[n] for n in dependencies ]) }
                    if len(dependencies) == 1:
                        loop_pattern = [ f'(?:{"|".join(expanded[dependencies.pop()])})+' ]
                    else:
                        loop_pattern = '|'.join([ ''.join([ f'(?:{"|".join(expanded[nn])}){{{n}}}' for nn in dependencies ]) for n in range(1, 10) ])
                    expanded[cur_rule] = chunks | { f'(?&RULE{cur_rule})' }
                    expanded[f'RULE{cur_rule}'] = f'(?P<RULE{cur_rule}>(?:{"".join(loop_pattern)}))'
                else:
                    expanded[cur_rule] = { x for n in rules[cur_rule] for x in reduce(_merge, [ expanded[nn] for nn in n ]) }
        remaining = rules.keys() - expanded.keys()
    return expanded


def part1(valid: set, messages: list) -> int:
    return len([ m for m in messages if m in valid ])


def part2(expanded: dict, messages: list) -> int:
    noregex = { e for e in expanded[0] if '(?&RULE' not in e }
    named_group_definitions = ''.join([ expanded[f'RULE{n}'] for n in (8, 11) ])
    pattern = '|'.join([ e for e in expanded[0] if '(?&RULE' in e ])
    pattern = f'^(?:{pattern})$'
    pattern = ''.join([ '(?V1)(?(DEFINE)', named_group_definitions, ')', pattern ])  # use regex version 1
    pattern: Pattern = regex.compile(pattern)
    return len([ m for m in messages if m in noregex or pattern.match(m) ])


if __name__ == '__main__':
    with open('input.txt') as f:
        rules, messages = f.read().split('\n\n')
        rules = { int(n): _dependencies(w.strip()) for n, w in map(lambda x: x.split(':'), [ r for r in rules.split('\n') ]) }
        messages = messages.strip().split('\n')
    print(part1(set(_expand(rules)[0]), messages))  # 265
    rules[8] += [[ 42, 8 ]]
    rules[11] += [[ 42, 11, 31 ]]
    print(part2(_expand(rules), messages))  # 394
