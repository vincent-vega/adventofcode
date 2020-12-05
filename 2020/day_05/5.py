#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def _seat_id(row: int, col: int) -> int:
    return row * 8 + col


def _row(boarding_pass: str) -> int:
    return _bisect(boarding_pass[:7])


def _col(boarding_pass: str) -> int:
    return _bisect(boarding_pass[7:])


def _bisect(sequence: str) -> int:
    return int(''.join([ '0' if s in 'FL' else '1' for s in sequence ]), 2)


"""
def _bisect_slow(sequence: str, selector_char: str) -> int:
    low, high = 0, 2**len(sequence) - 1
    for c in sequence:
        if c == selector_char:
            high = high - (high - low) // 2 - 1
        else:
            low = low + (high - low) // 2 + 1
    assert low == high
    return low
"""


def part1(seats: set) -> int:
    return max(seats)


def part2(seats: set) -> set:
    return set(range(min(seats), max(seats) + 1)) - seats


if __name__ == '__main__':
    with open('input.txt') as f:
        seats = { _seat_id(_row(v), _col(v)) for v in f.read().splitlines() }
    print(part1(seats))  # 896
    print(part2(seats))  # 659
