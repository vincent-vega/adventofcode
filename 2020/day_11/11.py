#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def _count_occupied(ferry: dict, seats: list) -> list:
    return [ c for c in seats if ferry.get(c) == '#' ]


def _update_seat(current: str, occupied: int, limit: int) -> str:
    if current == 'L' and occupied == 0:
        return '#'
    elif current == '#' and occupied >= limit:
        return 'L'
    return current


def _update_ferry(ferry: dict, topography: dict, limit: int) -> dict:
    return { coord: _update_seat(ferry[coord], len(_count_occupied(ferry, topography[coord])), limit) for coord in ferry.keys() }


def _visible_from(ferry: dict, coord: (int, int), X: int, Y: int) -> list:
    x, y = coord
    v = []
    # top
    xx = x
    for yy in range(y - 1, -1, -1):
        if (xx, yy) in ferry:
            v.append((xx, yy))
            break
    # bottom
    for yy in range(y + 1, Y + 1):
        if (xx, yy) in ferry:
            v.append((xx, yy))
            break
    # right
    yy = y
    for xx in range(x + 1, X + 1):
        if (xx, yy) in ferry:
            v.append((xx, yy))
            break
    # left
    for xx in range(x - 1, -1, -1):
        if (xx, yy) in ferry:
            v.append((xx, yy))
            break
    # top right
    xx, yy = x + 1, y - 1
    while xx <= X and yy >= 0:
        if (xx, yy) in ferry:
            v.append((xx, yy))
            break
        xx, yy = xx + 1, yy - 1
    # top left
    xx, yy = x - 1, y - 1
    while xx >= 0 and yy >= 0:
        if (xx, yy) in ferry:
            v.append((xx, yy))
            break
        xx, yy = xx - 1, yy - 1
    # bottom right
    xx, yy = x + 1, y + 1
    while xx <= X and yy <= Y:
        if (xx, yy) in ferry:
            v.append((xx, yy))
            break
        xx, yy = xx + 1, yy + 1
    # bottom left
    xx, yy = x - 1, y + 1
    while xx >= 0 and yy <= Y:
        if (xx, yy) in ferry:
            v.append((xx, yy))
            break
        xx, yy = xx - 1, yy + 1
    return v


def _visible(ferry: dict) -> dict:
    X, _ = max(ferry.keys(), key=lambda k: k[0])
    _, Y = max(ferry.keys(), key=lambda k: k[1])
    return { k: _visible_from(ferry, k, X, Y) for k in ferry.keys() }


def _adj_from(ferry: dict, coord: (int, int), X: int, Y: int) -> list:

    def _valid(coord: (int, int), delta: (int, int)) -> bool:
        if delta == (0, 0):
            return False
        if x < 0 or y < 0:
            return False
        delta_x, delta_y = delta
        if x + delta_x > X or y + delta_y > Y:
            return False
        return True

    x, y = coord
    return [ (delta_x + x, delta_y + y) for delta_y in (-1, 0, 1) for delta_x in (-1, 0, +1) if _valid((x, y), (delta_x, delta_y)) ]


def _adjacent(ferry: dict) -> dict:
    X, _ = max(ferry.keys(), key=lambda k: k[0])
    _, Y = max(ferry.keys(), key=lambda k: k[1])
    return { k: _adj_from(ferry, k, X, Y) for k in ferry.keys() }


def _board(ferry: dict, topography: dict, limit: int) -> dict:
    prev = ferry
    ferry = _update_ferry(ferry, topography, limit)
    while ferry != prev:
        prev = ferry
        ferry = _update_ferry(ferry, topography, limit)
    return ferry


def part1(ferry: dict) -> int:
    ferry = _board(ferry, _adjacent(ferry), 4)
    return sum([ 1 for k in ferry.keys() if ferry[k] == '#' ])


def part2(ferry: dict) -> int:
    ferry = _board(ferry, _visible(ferry), 5)
    return sum([ 1 for k in ferry.keys() if ferry[k] == '#' ])


if __name__ == '__main__':
    with open('input.txt') as f:
        ferry = { (int(x), int(y)): spot for y, line in enumerate(f.read().splitlines()) for x, spot in enumerate(line) if spot == 'L' }
    print(part1(ferry))  # 2470
    print(part2(ferry))  # 2259
