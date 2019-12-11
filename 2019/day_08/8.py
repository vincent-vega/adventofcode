#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import product
from collections import Counter, defaultdict

def part1(values: list, L: int, H: int) -> int:
    layer_size = L*H
    layer = min([ Counter(values[i:i + layer_size]) for i in range(1, len(values), layer_size) ], key=lambda c: c[0])
    return layer[1]*layer[2]

def _draw(pixel: int) -> str:
    return '#' if pixel == 1 else ' '

def part2(values: list, L: int, H: int) -> str:
    I = defaultdict(lambda: 2)
    layer_size = L*H
    for i in range(0, len(values), layer_size):
        for row, col in filter(lambda x: I[(x[1], x[0])] == 2, product(range(H), range(L))):
            layer = values[i:i + layer_size]
            I[(col, row)] = layer[row*L + col]
    return '\n'.join([ ''.join([ _draw(I[k]) for k in I.keys() if k[1] == i ]) for i in range(H) ])

if __name__ == '__main__':
    with open('input.txt') as f:
        values = [ int(n) for n in f.read().splitlines()[0] ]
    print(part1(values, 25, 6)) # 2440
    print(part2(values, 25, 6)) # AZCJC

