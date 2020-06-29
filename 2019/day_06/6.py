#!/usr/bin/python3
# -*- coding: utf-8 -*-

from itertools import product


class Node:

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = set() if parent is None else set([ parent ])

    def add_parent(self, parent):
        self.parent.add(parent)


def part1(nodes, COM):
    def _count(node, step):
        return step + 1 + sum(_count(nodes[n], step + 1) for n in filter(lambda p: p in nodes, node.parent))
    return _count(COM, -1)


def part2(nodes, COM):

    def _get_paths(node, cur_path):
        cur_path.append(node.name)
        paths = list()
        if len(node.parent) > 0:
            for n in filter(lambda p: p in nodes, node.parent):
                paths = paths + _get_paths(nodes[n], list(cur_path))
        else:
            paths.append(cur_path)
        return paths

    path1, path2 = map(lambda l: l[::-1], filter(lambda p: 'YOU' in p or 'SAN' in p, _get_paths(COM, [])))
    for i, j in product(range(len(path1)), range(len(path2))):
        if path1[i] == path2[j]:
            return i + j - 2


if __name__ == '__main__':
    with open('input.txt') as f:
        orbits = list(map(lambda x: x.split(')'), f.read().splitlines()))
    nodes = {}
    for t0, t1 in orbits:
        if t0 in nodes:
            nodes[t0].add_parent(t1)
        else:
            nodes[t0] = Node(t0, t1)
        if t1 not in nodes:
            nodes[t1] = Node(t1)
    print(part1(nodes, nodes['COM']))  # 162816
    print(part2(nodes, nodes['COM']))  # 304
