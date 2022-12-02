#!/usr/bin/env python3
# -*- coding: utf-8 -*-

strategy1 = {
    'A': {  # rock
        'X': 3 + 1,  # rock
        'Y': 6 + 2,  # paper
        'Z': 3  # scissor
    },
    'B': {  # paper
        'X': 1,  # rock
        'Y': 3 + 2,  # paper
        'Z': 6 + 3  # scissor
    },
    'C': {  # scissor
        'X': 6 + 1,  # rock
        'Y': 2,  # paper
        'Z': 3 + 3  # scissor
    },
}

strategy2 = {
    'A': {  # rock
        'X': 3,  # lose
        'Y': 3 + 1,  # draw
        'Z': 6 + 2  # win
    },
    'B': {  # paper
        'X': 1,  # lose
        'Y': 3 + 2,  # draw
        'Z': 6 + 3  # wi
    },
    'C': {  # scissor
        'X': 2,  # lose
        'Y': 3 + 3,  # draw
        'Z': 6 + 1  # win
    },
}


def part1(rounds: list[tuple]) -> int:
    return sum(strategy1[other][me] for other, me in rounds)


def part2(rounds: list[tuple]) -> int:
    return sum(strategy2[other][me] for other, me in rounds)


if __name__ == '__main__':
    with open('input.txt') as f:
        guide = [ tuple(line.split()) for line in f.read().splitlines() ]
    print(part1(guide))  # 10624
    print(part2(guide))  # 14060
