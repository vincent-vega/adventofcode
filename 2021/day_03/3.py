#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List


class Occurrence:
    def __init__(self):
        self.count = { '0': 0, '1': 0 }

    def update(self, c: str):
        self.count[c] += 1

    def most(self, default: int=None) -> int:
        if default is None:
            assert self.count['0'] != self.count['1']
        if self.count['0'] == self.count['1']:
            return default
        return 0 if self.count['0'] > self.count['1'] else 1

    def s_most(self, default: int=None) -> str:
        return str(self.most(default))


def _count(values: List[str]) -> List[Occurrence]:
    bit_count = len(values[0])
    occurrences = [ Occurrence() for _ in range(bit_count) ]
    for v in values:
        for pos, bit in enumerate(v):
            occurrences[pos].update(bit)
    return occurrences


def part1(report: List[str]) -> int:
    bit_count = len(report[0])
    occurrences = _count(report)
    gamma = sum(2 ** (bit_count - pos) for pos, o in enumerate(occurrences, 1) if o.most())
    epsilon = gamma ^ (2 ** bit_count - 1)
    return gamma * epsilon


def _filter(values: List[str], pos: int, most: bool=True) -> List[str]:
    occurrences = _count(values)
    return list(filter(lambda v: v[pos] == occurrences[pos].s_most(1) if most else v[pos] != occurrences[pos].s_most(1), values))


def part2(report: List[str]) -> int:
    oxygen = list(report)
    for pos in range(len(report[0])):
        oxygen = _filter(oxygen, pos)
        if len(oxygen) < 2:
            break
    oxygen = int(oxygen.pop(), 2)
    co2 = list(report)
    for pos in range(len(report[0])):
        co2 = _filter(co2, pos, False)
        if len(co2) < 2:
            break
    co2 = int(co2.pop(), 2)
    return oxygen * co2


if __name__ == '__main__':
    with open('input.txt') as f:
        report = f.read().splitlines()
    print(part1(report))  # 1307354
    print(part2(report))  # 482500
