#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def _move(x: int, y: int, direction: int) -> (int, int):
    match direction:
        case 0:  # UP
            return (x, y - 1)
        case 1:  # RIGHT
            return (x + 1, y)
        case 2:  # DOWN
            return (x, y + 1)
        case 3:  # LEFT
            return (x - 1, y)


def _turn(direction: int) -> int:
    return (direction + 1) % 4


def part1(obstacles: set[(int, int)], limit: (int, int), guard: (int, int)) -> int:
    X, Y = limit
    gx, gy = guard
    direction = 0
    visited = set()
    while 0 <= gx <= X and 0 <= gy <= Y:
        visited.add((gx, gy))
        while (nxt := _move(gx, gy, direction)) in obstacles:
            direction = _turn(direction)
        gx, gy = nxt
    return len(visited)


def part2(obstacles: set[(int, int)], limit: (int, int), guard: (int, int)) -> int:
    X, Y = limit
    obstructions = { (ox, oy) for ox in range(X + 1) for oy in range(Y + 1) if (ox, oy) not in obstacles and (ox, oy) != guard }
    loops = 0
    for o in obstructions:
        mod_obstacles = obstacles.union({o})
        gx, gy = guard
        direction = 0
        visited = set()
        while 0 <= gx <= X and 0 <= gy <= Y:
            if ((gx, gy), direction) in visited:
                loops += 1
                break
            visited.add(((gx, gy), direction))
            while (nxt := _move(gx, gy, direction)) in mod_obstacles:
                direction = _turn(direction)
            gx, gy = nxt
    return loops


if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.read().splitlines()
        X = len(lines[0]) - 1
        Y = len(lines) - 1
        obstacles = set()
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == '#':
                    obstacles.add((x, y))
                elif c == '^':
                    guard = (x, y)
    print(part1(obstacles, (X, Y), guard))  # 4903
    print(part2(obstacles, (X, Y), guard))  # 1911
