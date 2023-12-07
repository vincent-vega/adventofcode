#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter, defaultdict
from functools import cmp_to_key

CARD1 = [ 'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2' ]
CARD2 = [ 'A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J' ]


def _strength(hand: str) -> int:
    c = Counter(hand)
    if len(c) == 1:
        return 6  # five of a kind
    elif len(c) == 2 and c[list(c.keys())[0]] in (1, 4):
        return 5  # four of a kind
    elif len(c) == 2 and c[list(c.keys())[0]] in (2, 3):
        return 4  # full house
    elif len(c) == 3 and sorted(c.values()) == [1, 1, 3]:
        return 3  # three of a kind
    elif len(c) == 3 and sorted(c.values()) == [1, 2, 2]:
        return 2  # two pair
    return 1 if len(c) == 4 else 0  # one pair / high card


def _cmp(h1: tuple[str, int], h2: tuple[str, int], cards: list[str]) -> int:
    h1, _ = h1
    h2, _ = h2
    v = cards.index(h2[0]) - cards.index(h1[0])
    if v == 0 and len(h1) > 1:
        return _cmp((h1[1:], _), (h2[1:], _), cards)
    return v


def part1(values: tuple[tuple[str, int]]) -> int:
    def cmp(h1: tuple[str, int], h2: tuple[str, int]) -> int:
        return _cmp(h1, h2, CARD1)
    H = defaultdict(list)
    for h, b in values:
        H[_strength(h)].append((h, b))
    winnings = 0
    rank = 1
    for k in sorted(H):
        for _, bid in sorted(H[k], key=cmp_to_key(cmp)):
            winnings += rank * bid
            rank += 1
    return winnings


def _convert(hand: str) -> str:
    c = Counter(filter(lambda h: h != 'J', hand))
    if c:
        h, _ = max(c.items(), key=lambda x: x[1])
        return hand.replace('J', h)
    return 'AAAAA'


def part2(values: tuple[tuple[str, int]]) -> int:
    def cmp(h1: tuple[str, int], h2: tuple[str, int]) -> int:
        return _cmp(h1, h2, CARD2)
    H = defaultdict(list)
    for h, b in values:
        H[_strength(_convert(h) if 'J' in h else h)].append((h, b))
    winnings = 0
    rank = 1
    for k in sorted(H):
        for _, bid in sorted(H[k], key=cmp_to_key(cmp)):
            winnings += rank * bid
            rank += 1
    return winnings


if __name__ == '__main__':
    with open('input.txt') as f:
        values = tuple(map(lambda x: (x[0], int(x[1])), ( line.split() for line in f.read().splitlines() )))
    print(part1(values))  # 251136060
    print(part2(values))  # 249400220
