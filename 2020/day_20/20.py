#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce
import re


def _inverted(border: tuple) -> tuple:
    return tuple(9 - x for x in border[::-1])


def _parse_border_Y(tile: dict, up: bool) -> tuple:
    return tuple(sorted([ x for x, y in tile if y == 0 ])) if up else tuple(sorted([ x for x, y in tile if y == 9 ]))


def _parse_border_X(tile: dict, right: bool) -> tuple:
    return tuple(sorted([ y for x, y in tile if x == 9 ])) if right else tuple(sorted([ y for x, y in tile if x == 0 ]))


def part1(tiles: dict) -> int:
    border = { n: [ _parse_border_Y(t, True), _parse_border_X(t, True), _parse_border_Y(t, False), _parse_border_X(t, False) ] for n, t in tiles.items() }

    def _count_match(tile_border: tuple, others: tuple) -> int:
        return len([ 1 for b in tile_border if b in others or _inverted(b) in others ])
    return reduce(lambda a, b: a * b, [ n for n, b in border.items() if _count_match(b, { b for nn, bb in border.items() for b in bb if n != nn }) == 2 ])


if __name__ == '__main__':
    tiles = {}
    with open('input.txt') as f:
        for tile in f.read().strip().split('\n\n'):
            num, tile = tile.split(':\n')
            num = list(map(int, re.findall('\\d+', num))).pop()
            tiles[num] = { (x, y): True for y, line in enumerate(tile.split('\n')) for x, c in enumerate(line) if c == '#' }
    print(part1(tiles))  # 18411576553343
