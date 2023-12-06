#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce


def _adjacent(x: int, y: int) -> set((int, int)):
    return { (x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0) }


def part1(engine: dict) -> int:
    return sum([ n for n, adj in engine['parts'] if adj.intersection(engine['symbols']) ])


def part2(engine: dict) -> int:
    R = 0
    for x, y in engine['*']:
        num_id = { engine['num_id'][n] for n in _adjacent(x, y).intersection(engine['num']) }
        if len(num_id) == 2:
            R += reduce(lambda a, b: a * b, map(lambda i: engine['mapping'][i], num_id))
    return R


def _parse(lines: list[str]) -> dict:
    engine = { 'symbols': set(), '*': set(), 'parts': [], 'num': {}, 'num_id': {}, 'mapping': {} }
    cur_id = 0
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c.isdigit():
                if x + 1 < len(line) and line[x + 1].isdigit():
                    continue
                num = int(c)
                coord = { (x, y) }
                xx = x - 1
                p = 10
                adj = _adjacent(x, y)
                while line[xx].isdigit():
                    coord.add((xx, y))
                    num += int(line[xx]) * p
                    adj = adj.union(_adjacent(xx, y))
                    p *= 10
                    xx -= 1
                engine['parts'].append((num, adj))
                engine['mapping'][cur_id] = num
                for c in coord:
                    engine['num'][c] = num
                    engine['num_id'][c] = cur_id
                cur_id += 1
            elif c != '.':
                engine['symbols'].add((x, y))
                if c == '*':
                    engine['*'].add((x, y))
    return engine


if __name__ == '__main__':
    with open('input.txt') as f:
        engine = _parse(f.read().splitlines())
    print(part1(engine))  # 527446
    print(part2(engine))  # 73201705
