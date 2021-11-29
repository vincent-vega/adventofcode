#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict, deque, namedtuple
from copy import deepcopy
from functools import lru_cache
from typing import Dict, List, Set, Tuple

Coord = Tuple[int, int]
Finder = namedtuple('Finder', [ 'x', 'y', 'steps', 'start' ])


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


def _rearrange(units: List[Unit]) -> List[Unit]:
    return sorted([ u for u in units if u.hp ], key=lambda u: (u.y, u.x))


def _valid(x: int, y: int, wall: Set[Coord], units: Set[Coord]) -> bool:
    return x > 0 and y > 0 and (x, y) not in wall and (x, y) not in units


@lru_cache(maxsize=1024)
def _adjacent(x: int, y: int) -> Tuple[Coord]:
    return (x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)


def _parse_target(target: Set[Unit]) -> Dict[Coord, List[Unit]]:
    target_mapping = defaultdict(list)
    for t in target:
        for x, y in _adjacent(t.x, t.y):
            target_mapping[x, y].append(t)
    return target_mapping


def _next(u: Unit, others: Set[Unit], target_adj: Set[Coord], wall: Set[Coord]) -> Coord:
    F = []
    min_path_found = None
    Q = deque([ Finder(x, y, 1, (x, y)) for x, y in _adjacent(u.x, u.y)])  # finders need to be spawned in reading order
    others = { (o.x, o.y) for o in others }
    visited = { (u.x, u.y) }
    while Q:
        f = Q.popleft()
        if min_path_found is not None and f.steps > min_path_found:
            continue
        elif not _valid(f.x, f.y, wall, others):
            continue
        elif (f.x, f.y) in target_adj:
            min_path_found = f.steps if min_path_found is None else min(min_path_found, f.steps)
            F.append(f)
        elif (f.x, f.y) not in visited:
            visited.add((f.x, f.y))
            Q.extend([ Finder(x, y, f.steps + 1, f.start) for x, y in _adjacent(f.x, f.y) ])  # finders need to be spawned in reading order
    if not F:
        return u.x, u.y  # can't move
    return min(F, key=lambda f: (f.steps, f.y, f.x, f.start[1], f.start[0])).start


def _fight(units: List[Unit], wall: Set[Coord], interrupt_on_death: bool=False) -> Tuple[int, List[Unit]]:
    goblins = { u for u in units if u.type == 'G' }
    elves = { u for u in units if u.type == 'E' }
    rounds = 0
    while elves and goblins:
        units = _rearrange(units)
        for n, u in ((n, u) for n, u in enumerate(units, 1) if u.hp):
            target_mapping = _parse_target(goblins if u.type == 'E' else elves)
            if (u.x, u.y) not in target_mapping:
                # not in target range
                others = { other for other in units if (u.x, u.y) != (other.x, other.y) and other.hp }
                u.move(*_next(u, others, target_mapping.keys(), wall))
            if (u.x, u.y) in target_mapping:
                # attack
                target = min(target_mapping[u.x, u.y], key=lambda t: (t.hp, t.y, t.x))
                target.hp = max(0, target.hp - u.attack_power)
                if not target.hp:
                    if target.type == 'G':
                        goblins = { u for u in units if u.type == 'G' and u.hp }
                    else:
                        if interrupt_on_death:
                            return None, None
                        elves = { u for u in units if u.type == 'E' and u.hp }
                    if not elves or not goblins:
                        break
        if goblins and elves or n == len(units):
            rounds += 1
    return rounds, [ u for u in units if u.hp ]


def part1(units: List[Unit], wall: Set[Coord]) -> int:
    rounds, units = _fight(units, wall)
    return rounds * sum(u.hp for u in units)


def part2(units: List[Unit], wall: Set[Coord]) -> int:
    elf_attack_power = 4
    while True:
        for u in filter(lambda u: u.type == 'E', units):
            u.attack_power = elf_attack_power
        rounds, survivors = _fight(deepcopy(units), wall, True)
        if rounds is not None:
            return rounds * sum(s.hp for s in survivors)
        elf_attack_power += 1


def _parse(filename: str) -> Tuple[List[Unit], Set[Coord]]:
    with open(filename) as f:
        units = []
        wall = set()
        for y, line in enumerate(f.read().splitlines(), 1):
            for x, c in enumerate(line, 1):
                if c in 'EG':
                    units.append(Unit(c, x, y))
                elif c == '#':
                    wall.add((x, y))
    return units, wall


if __name__ == '__main__':
    units, wall = _parse('input.txt')
    print(part1(deepcopy(units), wall))  # 225096
    print(part2(units, wall))  # 35354
