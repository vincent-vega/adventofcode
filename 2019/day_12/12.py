#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce
from itertools import combinations, count
from math import gcd
import matplotlib.pyplot as plt
import re

def part1(moons: list, steps: int) -> int:
    for _ in range(steps):
        _run(moons)
    return sum([ m.potential_e()*m.kinetic_e() for m in moons ])

def part2(moons: list) -> int:
    # Moons' position/velocity are periodic
    # Interactions in each axis are independent
    # Calculate the period of each moon within each dimension separately
    periods = [ None, None, None ]
    start = [ [ m.get_axis_status(axis) for m in moons ] for axis in range(3) ]
    for c in count():
        if len([ 1 for p in periods if p is None ]) == 0:
            break
        _run(moons)
        for axis in range(3):
            if periods[axis] is None and [ m.get_axis_status(axis) for m in moons ] == start[axis]:
                periods[axis] = c + 1

    return reduce(_lcm, periods)

def _lcm(a, b):
    return abs(a*b) // gcd(a, b)

def _run(moons: list):
    for m1, m2 in combinations(moons, 2):
        g1, g2 = _gravities(m1, m2)
        m1.add_gravity(g1)
        m2.add_gravity(g2)
    for m in moons:
        m.move()

def _gravities(m1: 'Moon', m2: 'Moon') -> list:
    def _pull(x: (int, int)) -> int:
        return 1 if x[1] > x[0] else -1 if x[1] < x[0] else 0
    g1 = [ _pull(x) for x in zip(m1.location(), m2.location()) ]
    return g1, [ -1*x for x in g1 ]

class Moon:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def get_axis_status(self, axis: int) -> (int, int):
        return (self.x, self.vx) if axis == 0 else (self.y, self.vy) if axis == 1 else (self.z, self.vz)

    def location(self) -> list:
        return [ self.x, self.y, self.z ]

    def add_gravity(self, g: list):
        self.vx += g[0]
        self.vy += g[1]
        self.vz += g[2]

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def kinetic_e(self) -> int:
        return sum([ abs(i) for i in (self.vx, self.vy, self.vz) ])

    def potential_e(self) -> int:
        return sum([ abs(i) for i in (self.x, self.y, self.z) ])

def plot(moons: list):
    x = [ moons[0].x ]
    y = [ moons[0].y ]
    z = [ moons[0].z ]
    vx = [ moons[0].vx ]
    vy = [ moons[0].vy ]
    vz = [ moons[0].vz ]
    for _ in range(1000):
        _run(moons)
        x.append(moons[0].x)
        y.append(moons[0].y)
        z.append(moons[0].z)
        vx.append(moons[0].vx)
        vy.append(moons[0].vy)
        vz.append(moons[0].vz)

    plt.figure()

    plt.subplot(311)
    plt.title('x')
    plt.plot(x)

    plt.plot(vx, 'r--')

    plt.subplot(312)
    plt.title('y')
    plt.plot(y)

    plt.plot(vy, 'r--')

    plt.subplot(313)
    plt.title('z')
    plt.plot(z)

    plt.plot(vz, 'r--')
    plt.show()

if __name__ == '__main__':
    with open('input.txt') as f:
        moons = [ Moon(*p) for p in map(lambda l: [ int(x) for x in re.findall('-?\\d+', l) ], f.read().splitlines()) ]
    print(part1(list(moons), 1000)) # 14907
    print(part2(list(moons))) # 467081194429464

