#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def _fold(dots: set, axis: str, n: int) -> set:
    if axis == 'x':
        return { (x if x < n else n - x + n, y) for x, y in dots }
    return { (x, y if y < n else n - y + n) for x, y in dots }


def part1(dots: set, folds: list) -> int:
    return len(_fold(dots, *folds[0]))


def part2(dots: set, folds: list) -> str:
    for axis, n in folds:
        dots = _fold(dots, axis, n)
    X = max(map(lambda x: x[0], dots)) + 1
    Y = max(map(lambda x: x[1], dots)) + 1
    return '\n'.join([ ''.join('#' if (x, y) in dots else ' ' for x in range(X)) for y in range(Y) ])


if __name__ == '__main__':
    with open('input.txt') as f:
        dots, folds = f.read().split('\n\n')
        dots = { (x, y) for x, y in map(lambda x: map(int, x.split(',')), dots.split()) }
        folds = [ (a[-1], int(b)) for a, b in map(lambda x: x.split('='), folds.strip().split('\n')) ]
    print(part1(dots, folds))  # 666
    print(part2(dots, folds))  # CJHAZHKU
