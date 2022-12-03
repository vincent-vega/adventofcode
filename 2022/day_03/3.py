#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def _priority(item: str) -> int:
    return ord(item) - 96 if item.islower() else ord(item) - 38


def part1(rucksacks: list[str]) -> int:
    rucksacks = [ (set(r[:len(r) // 2]), set(r[len(r) // 2:])) for r in rucksacks ]
    return sum(_priority(b1.intersection(b2).pop()) for b1, b2 in rucksacks)


def _badge(group: list[str]) -> int:
    return group[0].intersection(group[1]).intersection(group[2])


def part2(rucksacks: list[str]) -> int:
    return sum(_priority(_badge([ set(r) for r in rucksacks[i:i + 3] ]).pop()) for i in range(0, len(rucksacks), 3))


if __name__ == '__main__':
    with open('input.txt') as f:
        rucksacks = f.read().splitlines()
    print(part1(rucksacks))  # 7742
    print(part2(rucksacks))  # 2276
