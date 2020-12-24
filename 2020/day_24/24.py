#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter


def _adj(x: int, y: int, cache: dict={}) -> set:
    if (x, y) in cache:
        return cache[(x, y)]
    cache[(x, y)] = { (x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx != dy }
    return cache[(x, y)]


def _flip(floor: dict) -> dict:
    nxt = {}
    adj_freq = Counter([ a for coord in floor for a in _adj(*coord) ])
    for coord, black_cnt in adj_freq.items():
        is_black = floor.get(coord)
        if is_black and (black_cnt == 1 or black_cnt == 2):
            nxt[coord] = True
        elif not is_black and black_cnt == 2:
            nxt[coord] = True
    return nxt


def _flip_deltas(delta: list) -> dict:
    floor = {}
    for d in delta:
        coord = (sum([ x for x, _ in d ]), sum([ y for _, y in d ]))
        floor[coord] = not floor[coord] if coord in floor else True
    return floor


def _parse(directions: str) -> list:
    i, deltas = 0, []
    while i < len(directions):
        if directions[i] in 'ew':
            deltas.append((-1, 0) if directions[i] == 'w' else (1, 0))
        elif directions[i] == 'n':
            deltas.append((-1, 1) if directions[i + 1] == 'w' else (0, 1))
        else:
            deltas.append((0, -1) if directions[i + 1] == 'w' else (1, -1))
        i += 1 if directions[i] in 'ew' else 2
    return deltas


def part1(delta: list) -> int:
    return len([ 1 for is_black in _flip_deltas(delta).values() if is_black ])


def part2(delta: list, rounds: int=100) -> int:
    floor = { c: True for c, is_black in _flip_deltas(delta).items() if is_black }
    for _ in range(rounds):
        floor = _flip(floor)
    return len(floor)


if __name__ == '__main__':
    with open('input.txt') as f:
        delta = [ _parse(line) for line in f.read().splitlines() ]
    print(part1(delta))  # 232
    print(part2(delta))  # 3519
