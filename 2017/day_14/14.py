#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce


def _hash(cord: list, values: list, skip: int=0, cur: int=0) -> (list, int, int):
    for v in values:
        assert v <= len(cord), 'Invalid length'
        if cur + v < len(cord):
            sub = cord[cur:cur + v]
            cord = cord[:cur] + sub[::-1] + cord[cur + v:]
        else:
            epilogue_len = len(cord) - cur
            sub = cord[cur:] + cord[:v - (len(cord) - cur)]
            prologue_len = len(sub) - epilogue_len
            sub = sub[::-1]
            cord = sub[epilogue_len:] + cord[prologue_len:cur] + sub[:epilogue_len]
        cur = (cur + v + skip) % len(cord)
        skip += 1
    return cord, skip, cur


def _knot_hash(inputstr: str) -> str:
    inputstr = [ ord(v) for v in inputstr ] + [17, 31, 73, 47, 23]
    skip = cur = 0
    cord = list(range(256))
    for _ in range(64):
        cord, skip, cur = _hash(cord, inputstr, skip, cur)
    dense = [ reduce(lambda x, y: x ^ y, cord[i * 16:i * 16 + 16]) for i in range(16) ]
    return ''.join([ hex(d)[2:].zfill(2) for d in dense ]).strip()


def part1(keystr: str, size: int) -> int:
    return sum([ bin(int(_knot_hash(f'{keystr}-{n}'), 16))[2:].count('1') for n in range(size) ])


def _adj(x: int, y: int) -> list:
    return [ (x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if abs(dx) != abs(dy) ]


def _bits(hexadecimal: str) -> list:
     return [ int(n) for x in hexadecimal for n in bin(int(x, 16))[2:].zfill(4) ]


def part2(keystr: str, size: int) -> int:
    grid = [ _bits(_knot_hash(f'{keystr}-{n}')) for n in range(size) ]
    grid = { (x, y) for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == 1 }
    cnt = 0
    while grid:
        cnt += 1
        found = { grid.pop() }
        while True:
            found = { a for x, y in found for a in _adj(x, y) if a in grid }
            if not found:
                break
            grid -= found
    return cnt


if __name__ == '__main__':
    print(part1('hxtvlmkl', 128))  # 8214
    print(part2('hxtvlmkl', 128))  # 1093
