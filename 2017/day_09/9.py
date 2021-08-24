#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def part1(stream: str) -> int:
    nest_lvl = score = 0
    cancel = garbage = False
    for c in stream:
        if cancel:
            cancel = False
        elif c == '!':
            cancel = True
        elif not garbage and c == '<':
            garbage = True
        elif garbage and c == '>':
            garbage = False
        elif not garbage and c == '{':
            nest_lvl += 1
        elif not garbage and c == '}':
            score += nest_lvl
            nest_lvl -= 1
    return score


def part2(stream: str) -> int:
    cnt = 0
    cancel = garbage = False
    for c in stream:
        if cancel:
            cancel = False
        elif c == '!':
            cancel = True
        elif not garbage and c == '<':
            garbage = True
        elif garbage and c == '>':
            garbage = False
        elif garbage:
            cnt += 1
    return cnt


if __name__ == '__main__':
    with open('input.txt') as f:
        streams = f.read().splitlines()
    print(*[ part1(s) for s in streams ], sep='\n')  # 10820
    print(*[ part2(s) for s in streams ], sep='\n')  # 5547
