#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def part1(pairs: list[tuple[set]]) -> int:
    return sum(1 for s1, s2 in pairs if len(s1.intersection(s2)) in { len(s1), len(s2) })


def part2(pairs: list[tuple[set]]) -> int:
    return sum(1 for p1, p2 in pairs if p1.intersection(p2))


def _extend(section: str) -> set[int]:
    start, end = map(int, section.split('-'))
    return set(range(start, end + 1))


if __name__ == '__main__':
    with open('input.txt') as f:
        pairs = [ tuple(map(_extend, line.split(','))) for line in f.read().splitlines() ]
    print(part1(pairs))  # 453
    print(part2(pairs))  # 919
