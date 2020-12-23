#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from copy import deepcopy


class Cup:
    def __init__(self, label: int):
        self.label = label
        self.next = None


def _pickup(cups: dict, current: int) -> list:
    cur = cups[current].next
    return [ cur.label, cur.next.label, cur.next.next.label ]


def _destination(picked: list, current: int, M: int) -> int:
    destination = current - 1
    while destination in picked or destination < 1:
        destination = M if destination < 1 else destination - 1
    return destination


def _connect(cups: dict, picked: list, current: int, destination: int):
    cups[current].next = cups[picked[-1]].next
    cups[picked[-1]].next = cups[destination].next
    cups[destination].next = cups[picked[0]]


def _move(cups: dict, current: int, rounds: int) -> dict:
    M = max(cups)
    picked = _pickup(cups, current)
    for _ in range(rounds):
        _connect(cups, picked, current, _destination(picked, current, M))
        current = cups[current].next.label
        picked = _pickup(cups, current)
    return cups


def _final_order(cups: dict) -> int:
    ret = []
    cur = cups[1].next
    while cur.label != 1:
        ret.append(cur.label)
        cur = cur.next
    return int(''.join(map(str, ret)))


def _fillup(cups: dict, values: int, size: int):
    M = max(cups)
    cur = cups[values[-1]]
    for i in range(M + 1, size + 1):
        c = Cup(i)
        cups[i] = c
        cur.next = c
        cur = c
    cur.next = cups[values[0]]
    return cups


def part1(cups: dict, current: int) -> int:
    return _final_order(_move(cups, current, 100))


def part2(cups: dict, current: int) -> int:
    _move(cups, current, 10000000)
    return cups[1].next.label * cups[1].next.next.label


if __name__ == '__main__':
    with open('input.txt') as f:
        values = list(map(int, f.read().strip()))
    cups = { c: Cup(c) for c in values }
    for i, c in enumerate(values):
        next_value = values[(i + 1) % len(values)]
        cups[c].next = cups[next_value]
    print(part1(deepcopy(cups), values[0]))  # 68245739
    print(part2(_fillup(cups, values, 1000000), values[0]))  # 219634632000
