#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from itertools import combinations


def bron_kerbosch(network: dict[set[str]], current: set[str], candidates: set[str], excluded: set[str], cliques: list[set[str]]):
    if not candidates and not excluded:
        cliques.append(current)
        return
    for node in list(candidates):
        bron_kerbosch(
            network,
            current | { node },
            candidates & network[node],
            excluded & network[node],
            cliques
        )
        candidates.remove(node)
        excluded.add(node)


def part1(network: dict[set[str]]) -> int:
    filtered = { c for c in network if c[0] == 't' }
    return sum([ 1 for c1, c2, c3 in combinations(network, 3) if (c1 in filtered or c2 in filtered or c3 in filtered) and len({ c2, c3 } - network[c1]) == 0 and len({ c1, c3 } - network[c2]) == 0 and len({ c1, c2 } - network[c3]) == 0 ])


def _password(lan: set[str]) -> str:
    return ','.join(sorted(lan))


def part2(network: dict[set[str]]) -> str:
    cliques = []
    bron_kerbosch(network, set(), set(network.keys()), set(), cliques)
    return _password(max(cliques, key=len))


if __name__ == '__main__':
    with open('input.txt') as f:
        network = defaultdict(set)
        for c1, c2 in (tuple(line.split('-')) for line in f.read().splitlines()):
            network[c1].add(c2)
            network[c2].add(c1)
    print(part1(network))  # 893
    print(part2(network))  # cw,dy,ef,iw,ji,jv,ka,ob,qv,ry,ua,wt,xz
