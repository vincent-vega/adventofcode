#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def part1(commands: list) -> int:
    x, y = 0, 0
    for c, n in commands:
        if c == 'forward':
            x += n
        elif c == 'up':
            y -= n
        elif c == 'down':
            y += n
    return x * y


def part2(commands: list) -> int:
    x, y, aim = 0, 0, 0
    for c, n in commands:
        if c == 'forward':
            x += n
            y += aim * n
        elif c == 'up':
            aim -= n
        elif c == 'down':
            aim += n
    return x * y


def _parse(command: str) -> (str, int):
    c, n = command.split()
    return c, int(n)


if __name__ == '__main__':
    with open('input.txt') as f:
        commands = [ _parse(x) for x in f ]
    print(part1(commands))  # 1804520
    print(part2(commands))  # 1971095320
