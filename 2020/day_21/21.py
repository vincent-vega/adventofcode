#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def _possibilities(menu: list) -> dict:
    P = {}  # allergen -> possible ingredients
    for ingr, allerg in menu:
        for a in allerg:
            P[a] = P[a] & ingr if a in P else ingr
    return P


def part1(menu: list) -> int:
    ingredients = { i for ingr, _ in menu for i in ingr }
    no_allerg = ingredients - { i for ingr in _possibilities(menu).values() for i in ingr }
    return sum([ len(no_allerg & ingr) for ingr, _ in menu ])


def part2(menu: list) -> str:
    P = _possibilities(menu)
    mapping = {}
    while P:
        for allergen, ingredient in filter(lambda i: len(i[1]) == 1, P.items()):
            mapping[allergen] = ingredient.pop()
        mapped = set(mapping.values())
        P = { allergen: i - mapped for allergen, i in P.items() if allergen not in mapping }
    return ','.join([ ingredient for _, ingredient in sorted(mapping.items(), key=lambda i: i[0]) ])


if __name__ == '__main__':
    with open('input.txt') as f:
        menu = list(map(lambda t: (set(t[0].split(' ')), set(t[1][:-1].split(', '))), map(lambda l: l.split(' (contains '), f.read().splitlines())))
    print(part1(menu))  # 1685
    print(part2(menu))  # ntft,nhx,kfxr,xmhsbd,rrjb,xzhxj,chbtp,cqvc
