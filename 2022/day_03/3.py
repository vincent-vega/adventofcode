#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def _priority(item: str) -> int:
    return ord(item) - ord('a') + 1 if item.islower() else ord(item) - ord('A') + 27


def part1(rucksacks: list[str]) -> int:
    rucksacks = map(lambda r: (set(r[:len(r) // 2]), set(r[len(r) // 2:])), rucksacks)
    return sum(_priority(comp1.intersection(comp2).pop()) for comp1, comp2 in rucksacks)


def _badge(group: list[set[str]]) -> str:
    return group[0].intersection(group[1]).intersection(group[2]).pop()


def part2(rucksacks: list[str]) -> int:
    return sum(_priority(_badge(list(map(set, rucksacks[i:i + 3])))) for i in range(0, len(rucksacks), 3))


if __name__ == '__main__':
    with open('input.txt') as f:
        rucksacks = f.read().splitlines()
    print(part1(rucksacks))  # 7742
    print(part2(rucksacks))  # 2276
