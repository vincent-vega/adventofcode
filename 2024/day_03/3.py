#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re


def part1(memory: str) -> int:
    instructions = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', memory)
    result = 0
    for i in instructions:
        x, y = map(int, i)
        result += x * y
    return result


def part2(memory: str) -> int:
    instructions = re.findall(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)", memory)
    result = 0
    enabled = True
    for i in instructions:
        if i == 'do()':
            enabled = True
        elif i == "don't()":
            enabled = False
        elif enabled:
            x, y = map(int, re.findall(r'\d+', i))
            result += x * y
    return result


if __name__ == '__main__':
    with open('input.txt') as f:
        memory = f.read()
    print(part1(memory))  # 180233229
    print(part2(memory))  # 95411583
