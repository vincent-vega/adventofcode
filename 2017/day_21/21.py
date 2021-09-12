#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import sqrt


def _flip(square: str) -> str:
    return '/'.join([ s[::-1] for s in square.split('/') ])


def _rotate(square: str) -> str:
    square = square.split('/')
    size = len(square)
    return '/'.join([ ''.join([ square[c][r] for c in range(size - 1, -1, -1) ]) for r in range(size) ])


def _variations(square: str) -> list:
    variations = []
    for _ in range(4):
        square = _rotate(square)
        variations.append(square)
        variations.append(_flip(square))
    return variations


def _breakup(square: str) -> list:
    square = square.split('/')
    big_size = len(square)
    small_size = 2 if big_size % 2 == 0 else 3
    return [ '/'.join([ ''.join([ square[r * small_size + i][c * small_size + j] for j in range(small_size) ]) for i in range(small_size) ]) for r in range(big_size // small_size) for c in range(big_size // small_size) ]


def _merge(squares: list, debug: bool=False) -> str:
    squares = [ s.split('/') for s in squares ]
    squares_per_line = int(sqrt(len(squares)))
    square_lines_cnt = len(squares[0])
    tot_lines_cnt = squares_per_line * square_lines_cnt
    return '/'.join([ ''.join([ squares[r // square_lines_cnt * squares_per_line + s][r % square_lines_cnt] for s in range(squares_per_line) ]) for r in range(tot_lines_cnt) ])


def _enhance(rules: dict, square: str, cnt: int) -> str:
    for _ in range(cnt):
        square = _merge([ rules[x] for x in _breakup(square) ])
    return square


def part1(rules: dict, square: str, cnt: int) -> int:
    return sum([ 1 for c in _enhance(rules, square, cnt) if c == '#' ])


def part2(rules: dict, square: str, cnt: int) -> int:
    return sum([ 1 for c in _enhance(rules, square, cnt) if c == '#' ])


if __name__ == '__main__':
    with open('input.txt') as f:
        rules = { t: v for k, v in map(lambda x: x.split(' => '), f.read().splitlines()) for t in _variations(k) }
    print(part1(rules, '.#./..#/###', 5))  # 110
    print(part2(rules, '.#./..#/###', 18))  # 1277716
