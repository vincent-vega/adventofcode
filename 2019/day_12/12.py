#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

from itertools import combinations, count
from dataclasses import dataclass
import re

def _run(moons: list):
    for m1, m2 in combinations(moons, 2):
        g1, g2 = _gravities(m1, m2)
        m1.add_gravity(g1)
        m2.add_gravity(g2)
    for m in moons:
        m.move()

def part1(moons: list, steps: int) -> int:
    for _ in range(steps):
        _run(moons)
    return sum([ m.potential_e()*m.kinetic_e() for m in moons ])

def part2(moons: list) -> int:
    P = set()
    P.add(str([ m.signature() for m in moons ]))
    i = 0
    for i in count():
        _run(moons)
        L = str([ m.signature() for m in moons ])
        if L in P:
            return i
        P.add(L)

def _gravities(m1: 'Moon', m2: 'Moon') -> list:
    def _pull(x: (int, int)) -> int:
        return 1 if x[1] > x[0] else -1 if x[1] < x[0] else 0
    g1 = [ _pull(x) for x in zip(m1.location(), m2.location()) ]
    return g1, [ -1*x for x in g1 ]

@dataclass
class Moon:

    x: int
    y: int
    z: int

    vx: int = 0
    vy: int = 0
    vz: int = 0

    def signature(self) -> list:
        return [ self.x, self.y, self.z, self.vx, self.vy, self.vz ]

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

if __name__ == '__main__':
    with open('input.txt') as f:
    #with open('example.txt') as f:
        #moons = [ Moon(*map(int, p)) for p in  map(lambda l: [ x for x in re.findall('-?\\d+', l) ], f.read().splitlines()) ]
        moons = [ Moon(*p) for p in  map(lambda l: [ int(x) for x in re.findall('-?\\d+', l) ], f.read().splitlines()) ]
    #print(part1(list(moons), 10)) #
    print(part1(list(moons), 1000)) #
    print(part2(list(moons))) #

