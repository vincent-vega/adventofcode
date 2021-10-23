#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re


def _manhattan(a: (int, int), b: (int, int)) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _closest(locations: dict, target: (int, int)) -> int:
    min_distance = min_name = None
    for n, coordinate in locations.items():
        if coordinate == target:
            return n
        d = _manhattan(coordinate, target)
        if min_distance is None or min_distance > d:
            min_distance = d
            min_name = n
        elif min_distance == d:
            min_name = None
    return min_name


def part1(locations: dict, top_left: (int, int), bottom_right: (int, int)) -> int:
    min_X, min_Y = top_left
    max_X, max_Y = bottom_right
    counter = { n: 0 for n in range(len(locations)) }
    for x in range(min_X, max_X + 1):
        for y in range(min_Y, max_Y + 1):
            closest = _closest(locations, (x, y))
            if closest is None or counter[closest] < 0:
                continue
            if x == 0 or y == 0 or x == max_X or y == max_Y:
                counter[closest] = -1
            else:
                counter[closest] += 1
    return max(counter.values())


def _sum_distance(locations: dict, target: (int, int)) -> int:
    return sum(_manhattan(coordinate, target) for coordinate in locations.values())


def part2(locations: dict, top_left: (int, int), bottom_right: (int, int), max_distance: int) -> int:
    min_X, min_Y = top_left
    max_X, max_Y = bottom_right
    return sum([ 1 for x in range(min_X, max_X + 1) for y in range(min_Y, max_Y + 1) if _sum_distance(locations, (x, y)) < max_distance ])


if __name__ == '__main__':
    with open('input.txt') as f:
        locations = { n: tuple(map(int, re.findall(r'-?\d+', line))) for n, line in enumerate(f.read().splitlines()) }
    top_left = (min(locations.values(), key=lambda x: x[0])[0] - 1, min(locations.values(), key=lambda x: x[1])[1] - 1)
    bottom_right = (max(locations.values(), key=lambda x: x[0])[0] + 1, max(locations.values(), key=lambda x: x[1])[1] + 1)
    print(part1(locations, top_left, bottom_right))  # 4771
    print(part2(locations, top_left, bottom_right, 10_000))  # 39149
