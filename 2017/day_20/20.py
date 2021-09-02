#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import lru_cache
from collections import Counter, namedtuple
import re

Particle = namedtuple('Particle', [ 'position', 'velocity', 'acceleration' ])


def _parse(data: list) -> Particle:
    x, y, z, vx, vy, vz, ax, ay, az = data
    return Particle((x, y, z), (vx, vy, vz), (ax, ay, az))


@lru_cache(maxsize=None)
def _intensity(vector: (int, int, int)) -> int:
    return sum(map(lambda x: x * x, vector))


def part1(particles: list) -> int:
    n, *_ = min([ (n, _intensity(p.acceleration), _intensity(p.velocity), _intensity(p.position)) for n, p in enumerate(particles) ], key=lambda x: x[1:])
    return n


def _distance(p1: Particle, p2: Particle) -> int:
    return sum([ pow(j - k, 2) for j, k in zip(p1.position, p2.position) ])


def _process_distances(particles: dict) -> int:
    removed = set()  # particles that are moving away from everything else
    for n, (p, d) in particles.items():
        if d is None:
            particles[n] = (p, { nn: _distance(p, pp) for nn, (pp, _) in particles.items() if n != nn })
        else:
            nxt = { nn: _distance(p, pp) for nn, (pp, _) in particles.items() if n != nn }
            nxt = { nn: dd for nn, dd in nxt.items() if nn in d and dd <= d[nn] }
            if len(nxt) == 0:
                removed.add(n)
            else:
                particles[n] = (p, nxt)
    for n in removed:
        del particles[n]
    return len(removed)


def _move(tracked: dict) -> dict:
    return { n: (Particle(tuple(map(sum, zip(p.position, map(sum, zip(p.velocity, p.acceleration))))),
                          tuple(map(sum, zip(p.velocity, p.acceleration))),
                          p.acceleration), d) for n, (p, d) in tracked.items() }


def _prune_collisions(tracked: dict) -> dict:
    c = Counter([ p.position for p, _ in tracked.values() ])
    return { n: (p, d) for n, (p, d) in tracked.items() if c[p.position] == 1 }


@lru_cache(maxsize=None)
def _coherent(vector1: (int, int, int), vector2: (int, int, int)) -> bool:
    return all([ j * k >= 0 for j, k in zip(vector1, vector2) ])  # every velocity component has the same sign of the corresponding acceleration one


def part2(particles: list) -> int:
    assert len(set([ p.position for p in particles ])) == len([ p.position for p in particles ]), 'Collision detected at t0'
    tracked = { n: (p, None) for n, p in enumerate(particles) }
    cnt = 0
    coherent = False
    while tracked:
        tracked = _move(tracked)
        tracked = _prune_collisions(tracked)
        coherent = coherent or all([ _coherent(p.velocity, p.acceleration) for p, _ in tracked.values() ])
        if coherent:
            cnt += _process_distances(tracked)
    return cnt


if __name__ == '__main__':
    with open('input.txt') as f:
        particles = [ _parse(map(int, re.findall('-?\\d+', l))) for l in f.read().splitlines() ]
    print(part1(particles))  # 144
    print(part2(particles))  # 477
