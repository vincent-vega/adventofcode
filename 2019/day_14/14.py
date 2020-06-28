#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from math import ceil
import doctest


def part1(B: dict, C: dict, R: list) -> int:
    ore = _compute(B, C, R, defaultdict(int))
    return ore


def _compute(B: dict, C: dict, R: list, leftovers: dict) -> int:
    need = defaultdict(int)
    for (count, what) in R:
        if leftovers[what] > 0:
            m = min(count, leftovers[what])
            count -= m
            leftovers[what] -= m
        if what in B:
            need[what] += count
            continue
        n = _break_down(B, C, what, count, leftovers)
        for w in n:
            need[w] += n[w]
    return sum([ _how_much_ore(B, n, need[n]) for n in need ])


def _break_down(B: dict, C: dict, what: str, quantity: int, leftovers: dict) -> dict:
    need = defaultdict(int)
    if leftovers[what] > 0:
        m = min(quantity, leftovers[what])
        quantity -= m
        leftovers[what] -= m
    if quantity == 0:
        return need
    count, formula = C[what]
    factor = ceil(quantity / count)
    for (c, w) in formula:
        c *= factor  # XXX
        if w in B:
            need[w] += c
            continue
        if leftovers[w] > 0:
            m = min(c, leftovers[w])
            c -= m
            leftovers[w] -= m
        n = _break_down(B, C, w, c, leftovers)
        for w in n:
            need[w] += n[w]

    leftovers[what] += factor * count - quantity
    return need


def _how_much_ore(B: dict, what: str, need: int) -> int:
    """ Calculate the amount of ORE needed to get a basic element

    >>> basic = { 'A': (10, 3) }

    >>> _how_much_ore(basic, 'A', 11)
    6
    >>> _how_much_ore(basic, 'A', 10)
    3
    >>> _how_much_ore(basic, 'A', 9)
    3
    """

    count, ore = B[what]
    return ore * ceil(need / count)


def _parse(formula: str, howto: dict, basic: dict):
    from_ingredient, to_ingredient = [ s.strip() for s in formula.split('=>') ]
    how_much, what = to_ingredient.split(' ')
    if 'ORE' in from_ingredient:
        basic[what] = (int(how_much), int(from_ingredient.split(' ')[0]))
    else:
        howto[what] = (int(how_much), [ tuple([ int(s.strip().split(' ')[0]), s.strip().split(' ')[1] ]) for s in from_ingredient.split(',') ])


def _parse_result(formula: str, ingredients: list):
    from_ingredient, to_ingredient = [ s.strip() for s in formula.split('=>') ]
    assert to_ingredient == '1 FUEL'
    ingredients.extend([ tuple([ int(s.strip().split(' ')[0]), s.strip().split(' ')[1] ]) for s in from_ingredient.split(',') ])


if __name__ == '__main__':
    doctest.testmod()
    B = {}  # basic elements
    C = {}  # complex elements
    R = []  # fuel elements
    with open('input.txt') as f:
        for line in f.read().splitlines():
            _parse_result(line, R) if 'FUEL' in line else _parse(line, C, B)
    print(part1(B, C, R))  # 178154
