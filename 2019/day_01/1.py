#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def _getfuelmass(mass):
    f = mass//3 - 2
    return f if f > 0 else 0

def part1(masslist):
    return sum([ _getfuelmass(m) for m in masslist ])

def part2(masslist):
    f = 0
    for m in masslist:
        while m > 0:
            m = _getfuelmass(m)
            f += m
    return f

if __name__ == '__main__':
    with open('input.txt') as f:
        masslist = list(map(int, f.read().splitlines()))
    print(part1(masslist)) # 3408471
    print(part2(masslist)) # 5109803

