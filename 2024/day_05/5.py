#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from functools import cmp_to_key


def _sorted(rules: dict[int, set[int]], update: list[int]) -> bool:
    for i in range(len(update)):
        for j in range(i + 1, len(update)):
            if update[i] in rules[update[j]]:
                return False
    return True


def part1(rules: dict[int, set[int]], updates: list[list[int]]) -> int:
    return sum(u[len(u) // 2] for u in updates if _sorted(rules, u))


def part2(rules: dict[int, set[int]], updates: list[list[int]]) -> int:
    not_ordered = [ u for u in updates if not _sorted(rules, u) ]

    def cmp(a: int, b: int) -> int:
        return -1 if b in rules[a] else 1 if a in rules[b] else 0
    return sum(sorted(u, key=cmp_to_key(cmp))[len(u) // 2] for u in not_ordered)


if __name__ == '__main__':
    with open('input.txt') as f:
        R, U = f.read().split('\n\n')
        rules = defaultdict(set)
        for x, y in (map(int, r.split('|')) for r in R.splitlines()):
            rules[x].add(y)
        updates = [ list(map(int, u.split(','))) for u in U.splitlines() ]
    print(part1(rules, updates))  # 4637
    print(part2(rules, updates))  # 6370
