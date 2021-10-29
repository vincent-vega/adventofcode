#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Node:
    def __init__(self, num_sons: int, num_meta: int):
        self.num_sons = num_sons
        self.sons = []
        self.num_meta = num_meta
        self.meta = []

    def add_son(self, son: 'Node'):
        self.sons.append(son)

    def add_meta(self, meta: list):
        self.meta.extend(meta)

    def value(self) -> int:
        return sum(self.meta) if len(self.sons) == 0 else sum(self.sons[n - 1].value() for n in filter(lambda m: m - 1 < len(self.sons), self.meta))


def _sum_meta(node: Node) -> int:
    return sum(node.meta) + sum(_sum_meta(s) for s in node.sons)


def part1(root: Node) -> int:
    return _sum_meta(root)


def part2(root: Node) -> int:
    return root.value()


def _tree(license: list) -> Node:
    root = Node(*license[0:2])
    nodes = [ root ]
    idx = 2
    while idx < len(license):
        num_sons, num_meta = license[idx:idx + 2]
        n = Node(num_sons, num_meta)
        nodes[-1].add_son(n)
        idx += 2
        if num_sons > 0:
            nodes.append(n)
            continue
        n.add_meta(license[idx:idx + n.num_meta])
        idx += n.num_meta
        while nodes and nodes[-1].num_sons == len(nodes[-1].sons):
            n = nodes.pop()
            n.add_meta(license[idx:idx + n.num_meta])
            idx += n.num_meta
    return root


if __name__ == '__main__':
    with open('input.txt') as f:
        root = _tree(list(map(int, f.read().split())))
    print(part1(root))  # 44893
    print(part2(root))  # 27433
