#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict

WORD = 'XMAS'


def _check_cross(words: dict[str, set[tuple[int, int]]], start: tuple[int, int], orientation: int) -> bool:
    x, y = start
    for c in WORD:
        if (x, y) not in words[c]:
            return False
        if orientation in (1, 3):
            x += -1 if orientation == 3 else 1
        elif orientation in (0, 2):
            y += -1 if orientation == 0 else 1
    return True


def _check_diag(words: dict[str, set[tuple[int, int]]], start: tuple[int, int], orientation: int) -> bool:
    x, y = start
    for c in WORD:
        if (x, y) not in words[c]:
            return False
        x += -1 if orientation in (0, 3) else 1
        y += -1 if orientation in (0, 1) else 1
    return True


def part1(words: dict[str, set[tuple[int, int]]]) -> int:
    count = 0
    for x, y in words['X']:
        count += sum(1 for orientation in range(4) if _check_cross(words, (x, y), orientation))
        count += sum(1 for orientation in range(4) if _check_diag(words, (x, y), orientation))
    return count


def _check_x_mas(words: dict[str, set[tuple[int, int]]], center: tuple[int, int], orientation: int) -> bool:
    x, y = center
    match orientation:
        case 0:
            if (x - 1, y - 1) not in words['M'] or (x + 1, y - 1) not in words['M']:
                return False
            if (x + 1, y + 1) not in words['S'] or (x - 1, y + 1) not in words['S']:
                return False
        case 1:
            if (x + 1, y - 1) not in words['M'] or (x + 1, y + 1) not in words['M']:
                return False
            if (x - 1, y - 1) not in words['S'] or (x - 1, y + 1) not in words['S']:
                return False
        case 2:
            if (x - 1, y + 1) not in words['M'] or (x + 1, y + 1) not in words['M']:
                return False
            if (x - 1, y - 1) not in words['S'] or (x + 1, y - 1) not in words['S']:
                return False
        case 3:
            if (x - 1, y - 1) not in words['M'] or (x - 1, y + 1) not in words['M']:
                return False
            if (x + 1, y - 1) not in words['S'] or (x + 1, y + 1) not in words['S']:
                return False
    return True


def part2(words: dict[str, set[tuple[int, int]]]) -> int:
    count = 0
    for x, y in words['A']:
        count += sum(1 for orientation in range(4) if _check_x_mas(words, (x, y), orientation))
    return count


if __name__ == '__main__':
    words = defaultdict(set)
    with open('input.txt') as f:
        for y, line in enumerate(f.read().splitlines()):
            for x, c in enumerate(line):
                words[c].add((x, y))
    print(part1(words))  # 2517
    print(part2(words))  # 1960
