#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import namedtuple

Instruction = namedtuple('Instruction', [ 'direction', 'value' ])


def _turn(current: str, instr: Instruction) -> str:
    idx = 'NESW'.index(current)
    idx = (idx + instr.value // 90 * (-1 if instr.direction == 'L' else 1)) % 4
    return 'NESW'[idx]


def _turn_ship(ship: dict, instr: Instruction):
    ship['current'] = _turn(ship['current'], instr)


def _turn_waypoint(waypoint: dict, instr: Instruction) -> dict:
    return { _turn(k, instr): waypoint[k] for k in waypoint.keys() }


def _reversed(direction: str) -> str:
    reverse = { 'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E' }
    return reverse[direction]


def _move_waypoint(waypoint: dict, instr: Instruction) -> dict:
    if instr.direction not in 'NESW':
        return _turn_waypoint(waypoint, instr)
    if instr.direction in waypoint:
        waypoint[instr.direction] += instr.value
    else:
        waypoint[_reversed(instr.direction)] -= instr.value
    return waypoint


def part1(navigation: list) -> int:
    ship = { 'current': 'E', 'N': 0, 'E': 0, 'S': 0, 'W': 0 }
    for instruction in navigation:
        if instruction.direction in 'NSEW':
            ship[instruction.direction] += instruction.value
        elif instruction.direction == 'F':
            ship[ship['current']] += instruction.value
        else:
            _turn_ship(ship, instruction)
    return abs(ship['N'] - ship['S']) + abs(ship['E'] - ship['W'])


def part2(navigation: list) -> int:
    waypoint = { 'N': 1, 'E': 10 }
    ship = { 'current': 'E', 'N': 0, 'E': 0, 'S': 0, 'W': 0 }
    for instruction in navigation:
        if instruction.direction == 'F':
            for k in waypoint.keys():
                ship[k] += instruction.value * waypoint[k]
        else:
            waypoint = _move_waypoint(waypoint, instruction)
    return abs(ship['N'] - ship['S']) + abs(ship['E'] - ship['W'])


if __name__ == '__main__':
    with open('input.txt') as f:
        navigation = [ Instruction(l[:1], int(l[1:])) for l in f.read().splitlines() ]
    print(part1(navigation))  # 1710
    print(part2(navigation))  # 62045
