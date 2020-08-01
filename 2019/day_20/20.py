#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque, namedtuple


def part1(M: dict) -> int:
    Q = deque()
    visited = set()
    Finder = namedtuple('Finder', [ 'coord', 'steps' ])
    Q.append(Finder(next(filter(lambda k: M[k] == 'AA', M)), 0))
    while Q:
        cur = Q.popleft()
        visited.add(cur.coord)
        if M[cur.coord] == 'ZZ':
            return cur.steps
        for x, y in [ a for a in _get_adjacent(cur.coord, M) if a not in visited ]:
            Q.append(Finder((x, y), cur.steps + 1))
    return -1  # Not found


def _get_adjacent(coord: (int, int), M: dict) -> list:
    x, y = coord
    adj = [ (x + dx, y + dy) for dx, dy in [ (-1, 0), (1, 0), (0, -1), (0, 1) ] if M.get((x + dx, y + dy)) is not None ]
    if isinstance(M[coord], tuple):
        # gate
        adj.append(M[coord])
    return adj


def part2(M: dict) -> int:
    Q = deque()
    visited = set()
    Finder = namedtuple('Finder', [ 'level', 'coord', 'steps' ])
    Q.append(Finder(0, next(filter(lambda k: M[k] == 'AA', M)), 0))
    max_x, _ = max(M.keys(), key=lambda k: k[0])
    _, max_y = max(M.keys(), key=lambda k: k[1])
    while Q:
        cur = Q.popleft()
        visited.add((cur.level, *cur.coord))
        assert cur.level > -1
        if M[cur.coord] == 'ZZ' and cur.level == 0:
            return cur.steps
        adjacents = _get_adjacent2(cur.coord, M, (max_x, max_y), cur.level)
        for lev, x, y in [ (lev, x, y) for lev, x, y in adjacents if (lev, x, y) not in visited ]:
            Q.append(Finder(lev, (x, y), cur.steps + 1))
    return -1  # Not found


def _get_adjacent2(coord: (int, int), M: dict, max_size: (int, int), cur_lev: int) -> list:
    x, y = coord
    adj = [ (cur_lev, x + dx, y + dy) for dx, dy in [ (-1, 0), (1, 0), (0, -1), (0, 1) ] if M.get((x + dx, y + dy)) is not None ]
    if isinstance(M[coord], tuple):
        # gate
        if not _is_outer_gate(coord, max_size) or cur_lev > 0:
            adj.append((cur_lev + (-1 if _is_outer_gate(coord, max_size) else 1), *M[coord]))
    return adj


def _is_outer_gate(gate: (int, int), max_size: (int, int)) -> bool:
    max_x, max_y = max_size
    gate_x, gate_y = gate
    return gate_x == 2 or gate_x == max_x or gate_y == 2 or gate_y == max_y


def _get_h_adjacent(coord: (int, int)) -> tuple:
    x, y = coord
    return (x - 1, y), (x + 1, y)


def _parse(line: str, y: int, M: dict, v_gates_x: dict):
    for x in range(len(line)):
        if line[x] == '.' and (x, y) not in M:
            if x in v_gates_x:
                M[(x, y)] = ''.join(v_gates_x[x])
                del v_gates_x[x]
            else:
                M[(x, y)] = '.'
        elif 'A' <= line[x] <= 'Z':
            a1, a2 = _get_h_adjacent((x, y))
            for a in (a1, a2):
                ax, _ = a
                if ax < len(line) and line[ax] == '.':
                    # horizontal gate
                    gate_name = (line[ax - 2] + line[x]) if ax > x else (line[x] + line[ax + 2])
                    M[(ax, y)] = gate_name
                    break
            else:
                if x in v_gates_x.keys():
                    if M.get((x, y - 2)) == '.':
                        M[(x, y - 2)] = v_gates_x[x][0] + line[x]
                        del v_gates_x[x]
                    else:
                        v_gates_x[x].append(line[x])
                else:
                    a1x, _ = a1
                    a2x, _ = a2
                    if (a1x >= len(line) or a1x < len(line) and line[a1x] == ' ') and (a2x >= len(line) or a2x < len(line) and line[a2x] == ' '):
                        # first vertical gate letter
                        v_gates_x[x] = [ line[x] ]


def _connect_gates(M: dict):
    gates = [ (k, v) for k, v in M.items() if v is not None and v != '.' ]
    for coord, name in gates:
        couple = [ p for p, g in gates if g == name ]
        if len(couple) == 2:
            g1, g2 = couple
            M[coord] = g1 if g1 != coord else g2


if __name__ == '__main__':
    maze = {}
    with open('input.txt') as f:
        lines = f.read().splitlines()
        flags = {}
        for y in range(len(lines)):
            _parse(lines[y], y, maze, flags)
        _connect_gates(maze)
    print(part1(maze))  # 628
    print(part2(maze))  # 7506
