#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce


def _knot_hash(cord: list, values: list, skip: int=0, cur: int=0) -> list:
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


def part1(values: list) -> int:
    values = list(map(int, values.split(',')))
    cord, _, __ = _knot_hash(list(range(256)), values)
    return cord[0] * cord[1]


def part2(values: list) -> str:
    values = [ ord(v) for v in values ] + [17, 31, 73, 47, 23]
    skip = cur = 0
    cord = list(range(256))
    for _ in range(64):
        cord, skip, cur = _knot_hash(cord, values, skip, cur)
    dense = [ reduce(lambda x, y: x ^ y, cord[i * 16:i * 16 + 16]) for i in range(16) ]
    return ''.join([ hex(d)[2:].zfill(2) for d in dense ]).strip()


if __name__ == '__main__':
    with open('input.txt') as f:
        values = f.read().splitlines()
    print(*[ part1(v) for v in values ], sep='\n')  # 40132
    print(*[ part2(v) for v in values ], sep='\n')  # 35b028fe2c958793f7d5a61d07a008c8
