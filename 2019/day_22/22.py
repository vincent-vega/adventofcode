#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque
from doctest import testmod


def part1(deck: deque, operations: list) -> str:
    return _shuffle(deck, operations).index(2019)


def _shuffle(deck: deque, operations: list) -> deque:
    for op in operations:
        if 'stack' in op:
            deck.reverse()
        elif 'cut' in op:
            *_, size = op.split(' ')
            deck.rotate(-1 * int(size))
        elif 'increment' in op:
            *_, size = op.split(' ')
            deck = _deal_with_increment_N(deck, int(size))
    return deck


def _deal_with_increment_N(deck: deque, N: int) -> deque:
    """
    >>> _deal_with_increment_N(deque(range(10)), 3)
    deque([0, 7, 4, 1, 8, 5, 2, 9, 6, 3])
    """
    size = len(deck)
    result = deque([ None ] * size)
    pos = 0
    for card in deck:
        result[pos] = card
        pos = (pos + N) % size
    return result


if __name__ == '__main__':
    testmod()
    with open('input.txt') as f:
        operations = list(f.read().splitlines())
    print(part1(deque(range(10007)), operations))  # 3939
