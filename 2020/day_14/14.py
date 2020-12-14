#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import combinations
import re


def _binstr(n: int, padding: int=36) -> str:
    return bin(n)[2:].zfill(padding)


def _bitmask(mask: str, value: int) -> int:
    bin_val = _binstr(value)
    return int(''.join([ bin_val[i] if m == 'X' else mask[i] for i, m in enumerate(mask) ]), 2)


def _floating(mask: str, address: str) -> list:
    base_address = int(''.join([ address[i] if m == '0' else '1' if m == '1' else '0' for i, m in enumerate(mask) ]), 2)
    X_idx = [ m.start() for m in re.finditer('X', mask) ]
    powers = [ 2**(35 - x) for x in X_idx ]
    offsets = [ 0 ] + [ sum(cc) for i in range(1, len(powers) + 1) for cc in combinations(powers, i) ]
    return [ base_address + n for n in offsets ]


def part1(commands: list) -> int:
    mem = {}
    for dest, value in commands:
        if dest == 'mask':
            mask = value
        else:
            address = int(dest[4:len(dest) - 1])
            mem[address] = _bitmask(mask, int(value))
    return sum(mem.values())


def part2(commands: list) -> int:
    mem = {}
    for dest, value in commands:
        if dest == 'mask':
            mask = value
        else:
            value = int(value)
            address = int(dest[4:len(dest) - 1])
            for address in _floating(mask, _binstr(address)):
                mem[address] = value
    return sum(mem.values())


if __name__ == '__main__':
    with open('input.txt') as f:
        commands = [ command for command in map(lambda l: l.split(' = '), f.read().splitlines()) ]
    print(part1(commands))  # 13727901897109
    print(part2(commands))  # 5579916171823
