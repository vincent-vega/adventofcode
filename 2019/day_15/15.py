#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque, namedtuple
from copy import deepcopy
from intcode import Intcode, Intcode_State


def part1(program: list) -> int:
    visited = set((0, 0))
    Finder = namedtuple('Finder', [ 'coord', 'path', 'steps', 'intcode_state' ])
    finders = deque([ Finder(_next_coord((0, 0), d), [], 0, Intcode_State(program, [ d ])) for d in range(1, 5) ])
    while finders:
        father = finders.popleft()
        out = _move(father.intcode_state)
        if out == 2:
            return father.steps + 1
        if out == 0:
            continue
        for direction in range(1, 5):
            nxt = _next_coord(father.coord, direction)
            if nxt in visited:
                continue
            visited.add(nxt)
            child_state = deepcopy(father.intcode_state)
            child_state.input.append(direction)
            finders.appendleft(Finder(nxt, father.path + [ nxt ], father.steps + 1, child_state))
    return -1


def _move(state: Intcode_State) -> int:
    while not state.exit:
        if state.output:
            return state.output.pop()
        if state.input_req:
            from sys import exit
            print('input req')
            exit(1)
        Intcode.run(state)
    return None


def _next_coord(coord: (int, int), mov: int) -> (int, int):
    x, y = coord
    if mov == 1:
        y += 1
    elif mov == 2:
        y -= 1
    elif mov == 3:
        x -= 1
    elif mov == 4:
        x += 1
    return (x, y)


def part2(values):
    pass


if __name__ == '__main__':
    with open('input.txt') as f:
        values = list(map(int, f.read().split(',')))
    print(part1(list(values)))  #
    print(part2(values))  #
