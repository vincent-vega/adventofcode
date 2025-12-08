#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import cache, reduce
from math import gcd, sqrt
import pyperclip


@cache
def distance_3d(p1: tuple[int, int, int], p2: tuple[int, int, int]) -> float:
    '''
    Euclidean distance: https://en.wikipedia.org/wiki/Euclidean_distance
    '''
    return sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)


@cache
def adj(x: int, y: int) -> list[tuple[int, int]]:
    return [ (x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if abs(dx) != abs(dy) ]


@cache
def fulladj(x: int, y: int) -> list[tuple[int, int]]:
    return [ (x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0) ]


@cache
def manhattan(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1 - y2)


@cache
def lcm(a: tuple[int]) -> int:
    return reduce(lambda i, j: abs(i * j) // gcd(i, j), a)


def pcprint(s: str):
    pyperclip.copy(s)
    print(s)
