#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from copy import deepcopy


def _score(board: dict, last: int) -> int:
    return sum(set(k for rowcol in board for k, v in rowcol.items() if not v)) * last


def part1(draw: list, boards: list) -> int:
    for n in draw:
        for board in boards:
            won = False
            for rowcol in board:
                if n in rowcol and not rowcol[n]:
                    rowcol[n] = True
                    if not won and all(rowcol.values()):
                        won = True
            if won:
                return _score(board, n)


def part2(draw: list, boards: list) -> int:
    winning = set()
    for n in draw:
        for board_num, board in filter(lambda x: x[0] not in winning, enumerate(boards)):
            last_won = False
            for rowcol in board:
                if n in rowcol and not rowcol[n]:
                    rowcol[n] = True
                    if not last_won and all(rowcol.values()):
                        winning.add(board_num)
                        if len(winning) == len(boards):
                            last_won = True
            if last_won:
                return _score(board, n)


def _boards(lines: list) -> list:
    board_count = sum(1 for b in lines if b == '') + 1
    R = (len(lines) - board_count + 1) / board_count
    assert R.is_integer(), 'Invalid row count'
    R = int(R)
    C = len(lines[0].split())
    boards = []
    for n in range(board_count):
        col = [ {} for _ in range(C) ]
        b = [ c for c in col ]
        for r in range(n * R + n, n * R + n + R):
            numbers = list(map(int, lines[r].split()))
            b.append({ x: False for x in numbers })
            for c in range(C):
                col[c][numbers[c]] = False
        boards.append(b)
    return boards


if __name__ == '__main__':
    with open('input.txt') as f:
        draw, _, *boards = f.read().splitlines()
        draw = list(map(int, draw.split(',')))
        boards = _boards(boards)
    # print(part1(draw, deepcopy(boards)))  # 63552
    # print(part2(draw, boards))  # 9020
    assert part1(draw, deepcopy(boards)) == 63552
    assert part2(draw, boards) == 9020
