#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque


def _do(line: deque, move: str) -> None:
    if move[0] == 's':
        line.rotate(int(move[1:]))
    elif move[0] == 'x':
        i, j = map(int, move[1:].split('/'))
        line[i], line[j] = line[j], line[i]
    elif move[0] == 'p':
        i, j = map(lambda x: line.index(x), move[1:].split('/'))
        line[i], line[j] = line[j], line[i]
    else:
        raise Exception('Invalid move')


def _dance(line: deque, moves: list) -> str:
    for m in moves:
        _do(line, m)
    return ''.join(line)


def part1(line: deque, moves: list) -> str:
    return _dance(line, moves)


def part2(line: deque, moves: list, cnt: int) -> str:
    start = deque(line)
    seen = { ''.join(line) }
    for n in range(1, cnt + 1):
        state = _dance(line, moves)
        if state in seen:
            line = start
            for _ in range(cnt % n):
                state = _dance(line, moves)
            return state
        seen.add(state)
    return state


if __name__ == '__main__':
    with open('input.txt') as f:
        moves = ''.join(f.read().splitlines()).split(',')
    line = [ chr(ord('a') + n) for n in range(16) ]
    print(part1(deque(line), moves))  # 'kbednhopmfcjilag'
    print(part2(deque(line), moves, 1_000_000_000))  # 'fbmcgdnjakpioelh'
