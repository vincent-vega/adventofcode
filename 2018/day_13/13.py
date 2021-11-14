#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List
from copy import deepcopy

LEFT, STRAIGHT, RIGHT = 0, 1, 2


class Cart:
    def __init__(self, x: int, y: int, symbol: str):
        self.go = 0
        self.x = x
        self.y = y
        if symbol == '<':
            self.next = (x - 1, y)
        elif symbol == '>':
            self.next = (x + 1, y)
        elif symbol == '^':
            self.next = (x, y - 1)
        elif symbol == 'v':
            self.next = (x, y + 1)
        else:
            raise Exception('Invalid cart symbol')

    def _left(self) -> (int, int):
        c_x, c_y = self.next
        p_x, p_y = self.x, self.y
        if c_y == p_y:
            return c_x, c_y - 1 if c_x > p_x else c_y + 1
        return c_x + 1 if c_y > p_y else c_x - 1, c_y

    def _straight(self) -> (int, int):
        c_x, c_y = self.next
        p_x, p_y = self.x, self.y
        if c_y == p_y:
            return c_x + 1 if c_x > p_x else c_x - 1, c_y
        return c_x, c_y + 1 if c_y > p_y else c_y - 1

    def _right(self) -> (int, int):
        c_x, c_y = self.next
        p_x, p_y = self.x, self.y
        if c_y == p_y:
            return c_x, c_y + 1 if c_x > p_x else c_y - 1
        return c_x - 1 if c_y > p_y else c_x + 1, c_y

    def move(self, tracks: dict):
        adj = { a for a in tracks[self.next] if a != (self.x, self.y) }
        if len(adj) == 1:
            self.x, self.y = self.next
            self.next = adj.pop()
        else:
            if self.go == LEFT:
                nxt = self._left()
            elif self.go == STRAIGHT:
                nxt = self._straight()
            elif self.go == RIGHT:
                nxt = self._right()
            self.x, self.y = self.next
            self.next = nxt
            self.go = (self.go + 1) % 3


def _rearrange(carts: List[Cart]) -> List[Cart]:
    return sorted(carts, key=lambda c: (c.y, c.x))


def part1(tracks: dict, carts: List[Cart]) -> str:
    while True:
        for n, c in enumerate(carts):
            c.move(tracks)
            if (c.x, c.y) in { (cc.x, cc.y) for nn, cc in enumerate(carts) if n != nn }:
                return f'{c.x},{c.y}'
        carts = _rearrange(carts)


def part2(tracks: dict, carts: List[Cart]):
    while len(carts) > 1:
        crashed = set()
        for n, c in filter(lambda x: x[0] not in crashed, enumerate(carts)):
            c.move(tracks)
            if (c.x, c.y) in { (cc.x, cc.y) for nn, cc in enumerate(carts) if n != nn }:
                crashed.update([ nn for nn, cc in enumerate(carts) if (cc.x, cc.y) == (c.x, c.y) ])
        carts = _rearrange([ c for n, c in enumerate(carts) if n not in crashed ])
    c = carts.pop()
    return f'{c.x},{c.y}'


def _parse_map(lines: list) -> (dict, List[Cart]):
    carts = []
    tracks = {}
    for y, line in enumerate(lines):
        for x, c in filter(lambda e: e[1] in r'/-|+\<>^v', enumerate(line)):
            if c in '<>^v':
                carts.append(Cart(x, y, c))
            if c in '<>-':
                tracks[x, y] = ((x - 1, y), (x + 1, y))
            elif c in 'v^|':
                tracks[x, y] = ((x, y - 1), (x, y + 1))
            elif c == '+':
                tracks[x, y] = ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
            elif c == '\\':
                if x > 0 and line[x - 1] in '-+<>^v':
                    tracks[x, y] = ((x - 1, y), (x, y + 1))
                else:
                    tracks[x, y] = ((x + 1, y), (x, y - 1))
            elif c == '/':
                if x > 0 and line[x - 1] in '-+<>^v':
                    tracks[x, y] = ((x - 1, y), (x, y - 1))
                else:
                    tracks[x, y] = ((x + 1, y), (x, y + 1))
    return tracks, carts


if __name__ == '__main__':
    with open('input.txt') as f:
        tracks, carts = _parse_map(f.read().splitlines())
    print(part1(tracks, [ deepcopy(c) for c in carts ]))  # 130,104
    print(part2(tracks, carts))  # 29,83
