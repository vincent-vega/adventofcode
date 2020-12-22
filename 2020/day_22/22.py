#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def _score(deck: list) -> int:
    return sum([ (i + 1) * j for i, j in enumerate(deck[::-1]) ])


def _play_regular(deck1: list, deck2: list):
    while deck1 and deck2:
        c1, c2 = deck1.pop(0), deck2.pop(0)
        if c1 > c2:
            deck1 += [ c1, c2 ]
        else:
            deck2 += [ c2, c1 ]
    return deck1 if len(deck1) > 0 else deck2


def _play_recursive(deck1: list, deck2: list) -> tuple:
    seen = set()
    while deck1 and deck2:
        state = (tuple(deck1), tuple(deck2))
        if state in seen:
            return deck1 + deck2, []
        seen.add(state)
        c1, c2 = deck1.pop(0), deck2.pop(0)
        if len(deck1) >= c1 and len(deck2) >= c2:
            d1, _ = _play_recursive(deck1[:c1], deck2[:c2])
            if len(d1) > 0:
                deck1 += [ c1, c2 ]
            else:
                deck2 += [ c2, c1 ]
        elif c1 > c2:
            deck1 += [ c1, c2 ]
        else:
            deck2 += [ c2, c1 ]
    return deck1, deck2


def part1(deck1: list, deck2: list) -> int:
    return _score(_play_regular(list(deck1), list(deck2)))


def part2(deck1: list, deck2: list) -> int:
    d1, d2 = _play_recursive(list(deck1), list(deck2))
    return _score(d1 if len(d1) > 0 else d2)


if __name__ == '__main__':
    with open('input.txt') as f:
        deck1, deck2 = map(lambda x: x.strip().split('\n'), f.read().split('\n\n'))
    deck1 = [ int(deck1[i]) for i in range(1, len(deck1)) ]
    deck2 = [ int(deck2[i]) for i in range(1, len(deck2)) ]
    print(part1(deck1, deck2))  # 33403
    print(part2(deck1, deck2))  # 29177
