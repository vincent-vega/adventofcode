#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from itertools import product
from math import gcd, pi
import cmath

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
    return current, len([ u for u in universe if u not in collisions ])

def _get_asteroids(M: dict) -> list:
    return [ k for k in M.keys() if M[k] ]

def _get_station(M: dict) -> ((int, int), int):
    size_X = (min(M.keys(), key=lambda l: l[0])[0], max(M.keys(), key=lambda l: l[0])[0])
    size_Y = (min(M.keys(), key=lambda l: l[1])[1], max(M.keys(), key=lambda l: l[1])[1])
    return max([ _sieve(M, k, size_X, size_Y) for k in _get_asteroids(M) ], key=lambda x: x[1])

def part1(M: dict) -> int:
    return _get_station(M)[1]

def _get_polar(x: int, y: int) -> (float, float): # radius, phi
    c = complex(x, y)
    return cmath.polar(c)

def _get_cartesian(radius: float, angle: float) -> (int, int):
    r = cmath.rect(radius, angle)
    return int(round(r.real)), int(round(r.imag))

def _move_center(M: dict, center: (int, int)) -> dict:
    cx, cy = center
    P = defaultdict(list)
    for x, y in filter(lambda k: M[k] == True and k != center, M.keys()):
        r, phi = _get_polar(x - cx, y - cy)
        assert (x - cx, y - cy) == _get_cartesian(r, phi)
        P[phi] = sorted(P[phi] + [ r ], reverse=True)
    return P

def _recenter(x, y, center):
    cx, cy = center
    return x - cx, y - cy

def _get_next(M1: dict, last_phi: float) -> (float, float):
    boundaries = [ (0, -pi/2), (pi/2, 0), (pi, pi/2), (-pi/2, -pi) ] # IV I II III
    i = 0
    if last_phi is None:
        last_phi = -pi
    else:
        while i < len(boundaries):
            max_b, min_b = boundaries[i]
            if last_phi < max_b and last_phi >= min_b:
                break
            i += 1
    # same quadrant
    max_b, min_b = boundaries[i]
    Q = sorted(filter(lambda x: x > last_phi and x < max_b and x >= min_b, M1.keys())) # TODO unnecessary sorting?
    if len(Q) > 0:
        phi = Q[0]
        r = M1[phi].pop()
        if len(M1[phi]) == 0:
            del M1[phi]
        return r, phi
    # next quadrants
    ii = (i + 1)%len(boundaries)
    while ii != i:
        max_b, min_b = boundaries[ii]
        Q = sorted(filter(lambda x: x < max_b and x >= min_b, M1.keys())) # TODO unnecessary sorting?
        if len(Q) > 0:
            phi = Q[0]
            r = M1[phi].pop()
            if len(M1[phi]) == 0:
                del M1[phi]
            return r, phi
        ii = (ii + 1)%len(boundaries)
    return None

def part2(M: dict) -> int:
    count = 0
    station = _get_station(M)[0]
    print(f'station -> {station}')
    M1 = _move_center(M, station)
    last_phi = None
    last_asteroid = None
    for _ in range(200): # TODO
        last_asteroid = _get_next(M1, last_phi)
        last_phi = last_asteroid[1]
        ####################
        if _ in [0, 1, 2, 9, 19, 49, 99, 197, 198, 199]:
            relative = _get_cartesian(*last_asteroid)
            absolute = _recenter(*relative, tuple(-1* i for i in station))
            print(f'#{_ + 1}: {relative} => {absolute}')
        ####################
    x, y = _recenter(*_get_cartesian(*last_asteroid), tuple(-1* i for i in station))
    return 100*x + y

if __name__ == '__main__':
    M = defaultdict(bool)
    with open('input.txt') as f:
    #with open('example.txt') as f:
        lines = f.read().splitlines()
    for y, x in product(range(len(lines)), range(len(lines[0]))):
        M[(x, y)] = lines[y][x] == '#'
    print(part1(M)) # 263
    print(part2(M)) # 1110

