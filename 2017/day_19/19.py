#!/usr/bin/env python3
# -*- coding: utf-8 -*-

letters = { chr(ord('A') + n) for n in range(ord('Z') - ord('A') + 1) }


def _adj(x: int, y: int) -> set[tuple[int, int]]:
    return { (x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if abs(dx) != abs(dy) }


def _validate(diagram: list, cur: tuple[int, int], nxt: tuple[int, int]) -> bool:
    x, y = nxt
    if diagram[y][x] == ' ':
        return False
    c_x, c_y = cur
    if diagram[c_y][c_x] == '|' and x != c_x or diagram[c_y][c_x] == '-' and y != c_y:
        return False
    return True


def _nxt(seen: set, cur: tuple[int, int], diagram: list) -> tuple[int, int]:
    c_x, c_y = cur
    for x, y in filter(lambda nxt: _validate(diagram, cur, nxt), _adj(c_x, c_y)):
        if y == c_y and diagram[y][x] == '|':
            dx = x - c_x
            x += dx
            while diagram[y][x] == '|':
                x += dx
            if diagram[y][x] not in letters.union({ '+', '-' }):
                continue
        elif x == c_x and diagram[y][x] == '-':
            dy = y - c_y
            y += dy
            while diagram[y][x] == '-':
                y += dy
            if diagram[y][x] not in letters.union({ '+', '|' }):
                continue
        if (x, y) not in seen:
            seen.add((x, y))
            return x, y
    return None


def part1(diagram: list, cur: tuple[int, int]) -> str:
    seen = { cur }
    path = []
    while cur:
        x, y = cur
        if diagram[y][x] in letters:
            path.append(diagram[y][x])
        cur = _nxt(seen, cur, diagram)
    return ''.join(path)


def part2(diagram: list, cur: tuple[int, int]) -> int:
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
