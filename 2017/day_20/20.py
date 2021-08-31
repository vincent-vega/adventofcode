#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import lru_cache
from collections import namedtuple, Counter
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


@lru_cache(maxsize=None)
def _distance(p1: Particle, p2: Particle) -> int:
    return sum([ pow(j - k, 2) for j, k in zip(p1.position, p2.position) ])


def _distance_from_others(current: int, particles: list) -> dict:
    return { n: _distance(particles[n], particles[current]) for n, p in enumerate(particles) if n != current }


def _move(tracked: dict) -> dict:
    return { n: (Particle(tuple(map(sum, zip(p.position, map(sum, zip(p.velocity, p.acceleration))))), tuple(map(sum, zip(p.velocity, p.acceleration))), p.acceleration), d) for n, (p, d) in tracked.items() }


def _prune_collisions(tracked: dict) -> dict:
    c = Counter([ p.position for p, d in tracked.values() ])
    return { n: (p, d) for n, (p, d) in tracked.items() if c[p.position] == 1 }


def part2(particles: list) -> int:
    assert len(set([ p.position for p in particles ])) == len([ p.position for p in particles ]), 'Collision detected at t0'
    tracked = { n: (p, _distance_from_others(n, particles)) for n, p in enumerate(particles) }
    cnt = 0
    # while tracked:
    for _ in range(100):
        tracked = _move(tracked)
        tracked = _prune_collisions(tracked)
        n = len(tracked)
        # prune diverging from everything else
        cnt += n - len(tracked)
    return len(tracked)


if __name__ == '__main__':
    with open('input.txt') as f:
        particles = [ _parse(map(int, re.findall('-?\\d+', l))) for l in f.read().splitlines() ]
    print(part1(particles))  # 144
    print(part2(particles))  # 477
