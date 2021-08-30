#!/usr/bin/env python3
# -*- coding: utf-8 -*-

letters = { chr(ord('A') + n) for n in range(ord('Z') - ord('A') + 1) }


def _adj(x: int, y: int, delta: int) -> set:
    return { (x + dx, y + dy) for dx in (-1 * delta, 0, delta) for dy in (-1 * delta, 0, delta) if abs(dx) != abs(dy) }


def _not_space(diagram: dict, coord: (int, int)) -> bool:
    x, y = coord
    return diagram[y][x] != ' '


def _nxt(seen: set, cur: (int, int), diagram) -> (int, int):
    c_x, c_y = cur
    prev = diagram[c_y][c_x]
    for x, y in filter(lambda coord: _not_space(diagram, coord), _adj(c_x, c_y, 1)):
        c = diagram[y][x]
        if prev == '|':
            if x != c_x:
                continue
            if c == '-':
                dy = y - c_y
                y += dy
                while diagram[y][x] == '-':
                    y += dy
        elif prev == '-':
            if y != c_y:
                continue
            if c == '|':
                dx = x - c_x
                x += dx
                while diagram[y][x] == '|':
                    x += dx
        elif prev in letters.union({ '+' }) and x == c_x and c not in letters.union({ '|' }):
            continue
        elif prev in letters.union({ '+' }) and y == c_y and c not in letters.union({ '-' }):
            continue
        if (x, y) not in seen:
            seen.add((x, y))
            return x, y
    return None


def part1(diagram: list, cur: (int, int)) -> str:
    seen = { cur }
    path = []
    while cur:
        x, y = cur
        if diagram[y][x] in letters:
            path.append(diagram[y][x])
        cur = _nxt(seen, cur, diagram)
    return ''.join(path)


def part2(diagram: dict, cur: (int, int)) -> int:
    x, y = cur
    seen = { cur }
    cnt = 1
    while cur:
        cnt += abs(cur[0] - x) + abs(cur[1] - y)
        x, y = cur
        cur = _nxt(seen, cur, diagram)
    return cnt


if __name__ == '__main__':
    with open('input.txt') as f:
        diagram = f.read().splitlines()
    start = ([ x for x, c in enumerate(diagram[0]) if c == '|' ].pop(), 0)
    print(part1(diagram, start))  # GSXDIPWTU
    print(part2(diagram, start))  # 16100
