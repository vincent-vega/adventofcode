#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def part1(values: list[int]) -> int:
    return max(sum(elf) for elf in values)


def part2(values: list[int]) -> int:
    return sum(sorted(sum(elf) for elf in values)[-3:])


def _parse(elf: str) -> list:
    return list(map(int, elf.split()))


if __name__ == '__main__':
    with open('input.txt') as f:
        values = [ _parse(e) for e in f.read().split('\n\n') ]
    print(part1(values))  # 67450
    print(part2(values))  # 199357
