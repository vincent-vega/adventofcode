#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict, deque, namedtuple
from typing import Dict, List, Set, Tuple

Coord = Tuple[int, int]
Finder = namedtuple('Finder', [ 'x', 'y', 'path' ]) # TODO instead of path use steps + first move


class Unit:
    def __init__(self, unit_type: str, x: int, y: int):
        self.type = unit_type
        self.x = x
        self.y = y
        self.attack_power = 3
        self.hp = 200

    def move(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self): # TODO remove
        return f'{self.type} coord {self.x},{self.y} - {self.attack_power} att power {self.hp} HP'


def _rearrange(units: List[Unit]) -> List[Unit]:
    return sorted([ u for u in units if u.hp ], key=lambda u: (u.y, u.x))


def _valid(x: int, y: int, wall: Set[Coord], units: Set[Coord]) -> bool:
    return x > 0 and y > 0 and (x, y) not in wall and (x, y) not in units


def _parse_target(target: Set[Unit], wall: Set[Coord]) -> Dict[Coord, List[Unit]]:
    target_mapping = defaultdict(list)
    for t in target:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if abs(dx) != abs(dy) and _valid(t.x + dx, t.y + dy, wall, set()):
                    target_mapping[t.x + dx, t.y + dy].append(t)
    return target_mapping


def _next(u: Unit, others: Set[Unit], target_adj: Set[Coord], wall: Set[Coord], debug=False) -> Coord: # TODO remove debug
    F = []
    min_path_found = None
    Q = deque([ Finder(u.x + dx, u.y + dy, [ (u.x + dx, u.y + dy) ]) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if abs(dx) != abs(dy) ])
    others = { (o.x, o.y) for o in others }
    visited = { (u.x, u.y) }
    while Q:
        f = Q.popleft()
        if min_path_found is not None and len(f.path) > min_path_found:
            continue
        elif not _valid(f.x, f.y, wall, others):
            continue
        elif (f.x, f.y) in target_adj:
            min_path_found = len(f.path) if min_path_found is None else min(min_path_found, len(f.path))
            F.append(f)
        elif (f.x, f.y) not in visited:
            visited.add((f.x, f.y))
            Q.extend([ Finder(f.x + dx, f.y + dy, f.path + [ (f.x + dx, f.y + dy) ]) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if abs(dx) != abs(dy) ])
    if not F:
        return u.x, u.y # can't move
    # if debug:
        # print(*sorted(F, key=lambda f: (len(f.path), f.path[-1][1], f.path[-1][0], f.path[0][1], f.path[0][0]), reverse=True), sep='\n')
    return min(F, key=lambda f: (len(f.path), f.y, f.x, f.path[0][1], f.path[0][0])).path[0]


def part1(units: List[Unit], wall: Set[Coord]) -> int:
    goblins = { u for u in units if u.type == 'G' }
    elves = { u for u in units if u.type == 'E' }
    E, G = len(elves), len(goblins)
    rounds = 0
    while E > 0 and G > 0:
        units = _rearrange(units)
        for player, u in enumerate(units, 1):
            if player == len(units):
                rounds += 1
            target_mapping = _parse_target(goblins if u.type == 'E' else elves, wall)
            if (u.x, u.y) not in target_mapping:
                x, y = _next(u, { other for other in units if (u.x, u.y) != (other.x, other.y) and other.hp }, target_mapping.keys(), wall, rounds == 24)
                u.move(x, y)
            if (u.x, u.y) in target_mapping:
                target = min(target_mapping[u.x, u.y], key=lambda t: (t.hp, t.y, t.x))
                target.hp = max(0, target.hp - u.attack_power)
                if not target.hp:
                    if target.type == 'G':
                        G -= 1
                        goblins = { u for u in units if u.type == 'G' and u.hp }
                    else:
                        E -= 1
                        elves = { u for u in units if u.type == 'E' and u.hp }
                    if E == 0 or G == 0:
                        break
        # if rounds + 1 in (1, 2, 23, 24, 25, 26, 27, 28, 47):
        # print(f'\nR{rounds}')
        # _print(units, wall)
        # print([ f'{u.type}({u.x},{u.y}):{u.hp}' for u in sorted(units, key=lambda u: (u.y, u.x)) if u.hp ])
    # _print(units, wall)
    print(f'R {rounds} HP {sum(u.hp for u in units if u.hp)}')
    return rounds * sum(u.hp for u in units if u.hp)


def _print(units, wall):
    g = set()
    e = set()
    for u in filter(lambda u: u.hp > 0, units):
        if u.type == 'G':
            g.add((u.x, u.y))
        else:
            e.add((u.x, u.y))
    for y in range(1, 8):
        print(*[ '#' if (x, y) in wall else 'G' if (x, y) in g else 'E' if (x, y) in e else '.' for x in range(1, 8) ], sep='')


def part2() -> int:
    pass


def _parse_line(line: str, y) -> set:
    return { Unit(c, x, y) for x, c in enumerate(line, 1) if c in 'EG' }



def _test(filename, result):
    with open(filename) as f:
        unit = []
        wall = set()
        for y, line in enumerate(f.read().splitlines(), 1):
            for x, c in enumerate(line, 1):
                if c in 'EG':
                    unit.append(Unit(c, x, y))
                elif c == '#':
                    wall.add((x, y))
        r = part1(unit, wall)
    try:
        assert r == result, f'TEST {filename} KO -> {r}'
        print(f'TEST {filename} OK')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    _test('example27730.txt', 27730)
    _test('example36334.txt', 36334)
    _test('example39514.txt', 39514)
    _test('example27755.txt', 27755)
    _test('example28944.txt', 28944)
    _test('example18740.txt', 18740)
    '''
    with open('input.txt') as f:
        unit = []
        wall = set()
        for y, line in enumerate(f.read().splitlines(), 1):
            for x, c in enumerate(line, 1):
                if c in 'EG':
                    unit.append(Unit(c, x, y))
                elif c == '#':
                    wall.add((x, y))
    r = part1(unit, wall)
    assert r > 219681
    print(r)
    # print(part2())  #
    '''
