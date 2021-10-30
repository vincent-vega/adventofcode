#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque
import re


def _play(numplayers: int, nummarbles: int):
    score = { n: 0 for n in range(1, numplayers + 1) }
    circle = deque([ 0 ])
    for marble in range(1, nummarbles + 1):
        if marble % 23 == 0:
            player = marble % numplayers + 1
            score[player] += marble
            circle.rotate(7)
            score[player] += circle.pop()
            circle.rotate(-1)
            continue
        circle.rotate(-1)
        circle.append(marble)
    return max(score.values())


def part1(numplayers: int, nummarbles: int) -> int:
    return _play(numplayers, nummarbles)


def part2(numplayers: int, nummarbles: int) -> int:
    return _play(numplayers, nummarbles)


if __name__ == '__main__':
    with open('input.txt') as f:
        players, marbles = map(int, re.findall(f'\d+', f.read()))
        print(part1(players, marbles))  # 404502
        print(part2(players, marbles * 100))  # 3243916887
