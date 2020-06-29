#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re


def part1(min_N, max_N):
    def _rules(n):
        n = str(n)
        if len(n) != 6:
            return False
        found_double = False
        for i in range(len(n) - 1):
            if n[i] == n[i + 1]:
                found_double = True
            if int(n[i]) > int(n[i + 1]):
                return False
        else:
            return found_double

    return len([ x for x in range(min_N, max_N + 1) if _rules(x) ])


def part2(min_N, max_N):
    def _rules(n):
        n = str(n)
        if len(n) != 6:
            return False
        prev = None
        found_double = False
        for i in range(len(n) - 1):
            if n[i] == n[i + 1] and (i == len(n) - 2 or int(n[i + 1]) != int(n[i + 2])) and n[i] != prev:
                found_double = True
            if int(n[i]) > int(n[i + 1]):
                return False
            prev = n[i]
        else:
            return found_double

    return len([ x for x in range(min_N, max_N + 1) if _rules(x) ])


if __name__ == '__main__':
    with open('input.txt') as f:
        min_N, max_N = list(map(int, re.findall(r'\d+', f.read())))
    print(part1(min_N, max_N))  # 895
    print(part2(min_N, max_N))  # 591
