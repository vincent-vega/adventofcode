#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from functools import cache
import re


@dataclass
class Brick:
    x1: int
    y1: int
    z1: int
    x2: int
    y2: int
    z2: int

    def __hash__(self):
        return hash(tuple([ self.x1, self.y1, self.z1, self.x2, self.y2, self.z2 ]))


@cache
def _blocks(b: Brick) -> tuple[tuple[int]]:
    if b.x1 != b.x2:
        return tuple((i, b.y1, b.z1) for i in range(min(b.x1, b.x2), max(b.x1, b.x2) + 1))
    if b.y1 != b.y2:
        return tuple((b.x1, i, b.z1) for i in range(min(b.y1, b.y2), max(b.y1, b.y2) + 1))
    if b.z1 != b.z2:
        return tuple((b.x1, b.y1, i) for i in range(min(b.z1, b.z2), max(b.z1, b.z2) + 1))
    return tuple([ tuple([ b.x1, b.y1, b.z1 ]) ])


@cache
def _blocks_map(bricks: tuple[Brick]) -> dict[tuple[int], Brick]:
    return { block: brick for brick in bricks for block in _blocks(brick) }


@cache
def _stack(bricks: tuple[Brick]) -> tuple[Brick]:
    bricks = sorted(bricks, key=lambda b: min(b.z1, b.z2))
    W = {}  # top layer: maximum z for each x,y
    final = []
    for b in bricks:
        Z = 1
        minz = 0
        for x, y, z in _blocks(b):
            minz = z if not minz else min(minz, z)
            if (x, y) in W:
                Z = max(Z, W[x, y] + 1)
        for x, y, z in _blocks(b):
            W[x, y] = Z + z - minz if (x, y) not in W else max(W[x, y], Z + z - minz)
        z1 = Z if b.z1 <= b.z2 else Z + b.z1 - b.z2
        z2 = Z if b.z2 <= b.z1 else Z + b.z2 - b.z1
        final.append(Brick(b.x1, b.y1, z1, b.x2, b.y2, z2))
    return tuple(final)


def part1(bricks: tuple[Brick]) -> int:
    bricks = _stack(bricks)
    W = _blocks_map(bricks)
    to_be_removed = 0
    for b in bricks:
        seen = set()
        for c in filter(lambda c: c in W, map(lambda c: (c[0], c[1], c[2] + 1), _blocks(b))):
            upper_brick = W[c]
            if upper_brick in seen or upper_brick == b:
                continue
            seen.add(upper_brick)
            for (x, y, z) in _blocks(upper_brick):
                lower_block = (x, y, z - 1)
                if lower_block in W and W[lower_block] != b and W[lower_block] != upper_brick:
                    break  # upper_brick has another support different from b
            else:
                break  # b is the only support for upper_brick
        else:
            to_be_removed += 1
    return to_be_removed


def _supported_by(bricks: tuple[Brick]) -> dict[Brick, set[Brick]]:
    W = _blocks_map(bricks)
    supported_by = { b: set() for b in bricks }
    for b in bricks:
        for (x, y, z) in _blocks(b):
            higher_block = (x, y, z + 1)
            if higher_block in W and W[higher_block] != b:
                supported_by[b].add(W[higher_block])
    return supported_by


def _support(bricks: tuple[Brick]) -> dict[Brick, set[Brick]]:
    W = _blocks_map(bricks)
    support = { b: set() for b in bricks }
    for b in bricks:
        for (x, y, z) in _blocks(b):
            lower_block = (x, y, z - 1)
            if lower_block in W and W[lower_block] != b:
                support[b].add(W[lower_block])
    return support


def part2(bricks: tuple[Brick]) -> int:
    bricks = _stack(bricks)
    M = _supported_by(bricks)  # brick -> set[brick]: list of bricks supported by 'brick'
    N = _support(bricks)  # brick -> set[brick]: list of bricks which support 'brick'
    count = 0
    for b in bricks:
        remaining = set(bricks)
        to_be_removed = { b }
        while to_be_removed:
            x = to_be_removed.pop()
            remaining.remove(x)
            for m in (m for m in M[x] if m in remaining):
                if all(n not in remaining for n in N[m]):
                    to_be_removed.add(m)
        count += len(bricks) - len(remaining) - 1
    return count


if __name__ == '__main__':
    with open('input.txt') as f:
        bricks = tuple(map(lambda x: Brick(*tuple(map(int, re.findall(r'\d+', x)))), f.read().splitlines()))
    print(part1(bricks))  # 421
    print(part2(bricks))  # 39247
