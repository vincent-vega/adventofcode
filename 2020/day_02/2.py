#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter, namedtuple
import re

Rule = namedtuple('Rule', [ 'policy', 'letter', 'password' ])


def part1(rules: list) -> int:
    def check_rule(rule: Rule) -> bool:
        min_o, max_o = map(int, re.findall('\\d+', rule.policy))
        counter = Counter(rule.password)
        return False if counter[rule.letter] > max_o or counter[rule.letter] < min_o else True

    return len([ r for r in rules if check_rule(r) ])


def part2(rules: list) -> int:
    def check_rule(rule: Rule) -> bool:
        pos_1, pos_2 = map(lambda x: int(x) - 1, re.findall('\\d+', rule.policy))
        return True if (rule.password[pos_1] == rule.letter) ^ (rule.password[pos_2] == rule.letter) else False

    return len([ r for r in rules if check_rule(r) ])


if __name__ == '__main__':
    with open('input.txt') as f:
        rules = list(map(lambda r: Rule(*r), [ row.replace(':', '').split(' ') for row in f ]))
    print(part1(rules))  # 655
    print(part2(rules))  # 673
