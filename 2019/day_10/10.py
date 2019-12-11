#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from itertools import product
from math import gcd

def _get_colliding_spots(station: (int, int), asteroid: (int, int), X_size: (int, int), Y_size: (int, int)) -> list:
    min_X, max_X = X_size
    min_Y, max_Y = Y_size
    x_diff = asteroid[0] - station[0]
    y_diff = asteroid[1] - station[1]

    GCD = gcd(x_diff, y_diff)
    x_diff /= GCD
    y_diff /= GCD

    x, y = asteroid
    x += x_diff
    y += y_diff
    colliding_coord = []
    while x <= max_X and x >= min_X and y <= max_Y and y >= min_Y:
        colliding_coord.append((x, y))
        x += x_diff
        y += y_diff
    return colliding_coord

def _sieve(M: dict, current: (int, int), X_size: (int, int), Y_size: (int, int)) -> int:
    universe = [ a for a in _get_asteroids(M) if a != current ]
    collisions = set()
    collisions.update([ c for u in universe for c in _get_colliding_spots(current, u, X_size, Y_size) ])
    #if len([ u for u in universe if u not in collisions ]) == 263:
        #print(f'{current}')
    return len([ u for u in universe if u not in collisions ])

def _get_asteroids(M: dict) -> list:
    return [ k for k in M.keys() if M[k] ]

def _get_station_coordinates(M: dict) -> (int, int):
    pass # TODO

def part1(M: dict) -> int:
    size_X = (min(M.keys(), key=lambda l: l[0])[0], max(M.keys(), key=lambda l: l[0])[0])
    size_Y = (min(M.keys(), key=lambda l: l[1])[1], max(M.keys(), key=lambda l: l[1])[1])
    return max([ _sieve(M, k, size_X, size_Y) for k in _get_asteroids(M) ])

def part2(M: dict) -> int:
    #station_x, station_y = (23, 29)
    pass

if __name__ == '__main__':
    M = defaultdict(bool)
    with open('input.txt') as f:
        lines = f.read().splitlines()
    for y, x in product(range(len(lines)), range(len(lines[0]))):
        M[(x, y)] = lines[y][x] == '#'
    print(part1(M)) # 263
    print(part2(M)) #

