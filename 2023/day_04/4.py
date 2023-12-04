#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re


def _score(card: (set[int], set[int])) -> int:
    n = sum(1 for v in card[0] if v in card[1])
    return 0 if n == 0 else 2 ** (n - 1)


def part1(cards: list[tuple[set[int], set[int]]]) -> int:
    return sum(_score(card) for card in cards)


def part2(cards: dict[int, tuple[tuple[set[int], set[int]], int]]) -> int:
    for n, (card, count) in cards.items():
        win = sum(1 for v in card[0] if v in card[1])
        for i in filter(lambda i: i in cards, range(n + 1, n + win + 1)):
            card, cnt = cards[i]
            cards[i] = (card, cnt + count)
    return sum(n for _, n in cards.values())


def _parse(line: str) -> (set[int], set[int]):
    win, cur = line.split(' | ')
    return (set(map(int, re.findall(r'\d+', win.split(': ')[1]))), set(map(int, re.findall(r'\d+', cur))))


if __name__ == '__main__':
    with open('input.txt') as f:
        cards = [ _parse(line) for line in f.read().splitlines() ]
    print(part1(cards))  # 23678
    print(part2({ n: (card, 1) for n, card in enumerate(cards) }))  # 15455663
