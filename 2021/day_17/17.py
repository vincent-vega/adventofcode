#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
import re


def part1(target: set) -> int:
    minY = min([ y for _, y in target ])
    maxvY = abs(minY) - 1
    return sum(range(1, maxvY + 1))


def _horizontal(target: set) -> dict:
    findings = defaultdict(set)
    hrange = { c[0] for c in target }
    X = max(hrange)
    for vx in range(X, 0, -1):
        hist = list(range(vx, -1, -1))
        x_at_step = { (t, x) for t, x in map(lambda t: (t, sum(hist[:t])), range(1, len(hist))) if x in hrange }  # XXX len(hist) + 1?
        for step, x in x_at_step:
            findings[step].add((vx, x))
    return findings  # steps -> { (vx, finalX) ... }


def _vertical(target: set) -> dict:
    findings = defaultdict(set)
    vrange = { c[1] for c in target }
    minY = min(vrange)
    # Y velocities lower or equal to 0
    for vy in range(0, minY - 1, -1):
        hist = list(range(vy, minY - 1, -1))
        y_at_step = { (t, y) for t, y in map(lambda t: (t, sum(hist[:t])), range(1, len(hist) + 1)) if y in vrange }
        for step, y in y_at_step:
            findings[step].add((vy, y))
    # Y velocities greater than 0
    for vy in range(1, abs(minY)):
        hist = list(range(vy, 0, -1)) + list(range(0, -1 * (vy + 1), -1)) + list(range(-1 * (vy + 1), minY - 1, -1))
        y_at_step = { (t, y) for t, y in map(lambda t: (t, sum(hist[:t])), range(1, len(hist) + 1)) if y in vrange }
        for step, y in y_at_step:
            findings[step].add((vy, y))
    return findings  # steps -> { (vy, finalY) ... }


def part2(target: set) -> int:
    h_findings = _horizontal(target)
    v_findings = _vertical(target)
    velocities = set()
    for step, h_data in h_findings.items():
        velocities.update({ (vx, vy) for vx, _ in h_data for vy, _ in v_findings.get(step, set()) })
    # X velocities stopping on the target
    for step, h_data in h_findings.items():
        for vx, x in filter(lambda data: sum(range(1, data[0] + 1)) == data[1], h_data):
            velocities.update({ (vx, vy) for n, v_data in v_findings.items() for vy, y in v_data if n > step })
    return len(velocities)


if __name__ == '__main__':
    with open('input.txt') as f:
        mx, Mx, my, My = map(int, re.findall(r'-?\d+', f.read()))
        target = { (x, y) for x in range(mx, Mx + 1) for y in range(my, My + 1) }
    print(part1(target))  # 8646
    print(part2(target))  # 5945
