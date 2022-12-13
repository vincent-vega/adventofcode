#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import cmp_to_key
from typing import Union


def _lt(p1: Union[int, list], p2: Union[int, list]) -> int:
    for idx in range(max(len(p1), len(p2))):
        if idx == len(p1):
            return -1
        elif idx == len(p2):
            return 1
        v1, v2 = p1[idx], p2[idx]
        if isinstance(v1, int) and isinstance(v2, int) and v1 != v2:
            return -1 if v1 < v2 else 1
        elif isinstance(v1, list) and isinstance(v2, int) and (r := _lt(v1, [ v2 ])) != 0:
            return r
        elif isinstance(v1, int) and isinstance(v2, list) and (r := _lt([ v1 ], v2)) != 0:
            return r
        elif isinstance(v1, list) and isinstance(v2, list) and (r := _lt(v1, v2)) != 0:
            return r
    return 0


def part1(packets: list) -> int:
    return sum(n for n, (p1, p2) in enumerate(packets, 1) if _lt(p1, p2) < 0)


def part2(packets: list) -> int:
    packets = sorted([ p for pair in packets for p in pair ] + [ [[ 2 ]], [[ 6 ]] ], key=cmp_to_key(_lt))
    return (packets.index([[ 2 ]]) + 1) * (packets.index([[ 6 ]]) + 1)


def _parse(value: str, start: int) -> (list, int):
    packet = []
    end = start
    while end < len(value):
        if value[end] == '[':
            v, end = _parse(value, end + 1)
            packet.append(v)
        elif value[end] == ']':
            return packet, end + 1
        elif value[end] == ',':
            end += 1
            continue
        else:
            for e in range(end + 1, len(value)):
                if value[e] in ',]' and e > end:
                    packet.append(int(value[end:e]))
                    break
        end += 1
    return packet, end


def _packet(pkt: str) -> list:
    pkt, _ = _parse(pkt, 1)
    return pkt


if __name__ == '__main__':
    with open('input.txt') as f:
        # packets = [ tuple(map(eval, pair.strip().split('\n'))) for pair in f.read().split('\n\n') ]  # using `eval' function
        packets = [ tuple(map(lambda p: _packet(p), pair.strip().split('\n'))) for pair in f.read().split('\n\n') ]  # custom parser
    print(part1(packets))  # 5292
    print(part2(packets))  # 23868
