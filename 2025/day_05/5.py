#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def part1(fresh: list[tuple[int, int]], ingredients: set[int]) -> int:
    return len(set(n for (m, M) in fresh for n in filter(lambda n: m <= n <= M, ingredients)))


def part2(fresh: list[tuple[int, int]]) -> int:
    start_idx = 0
    while True:
        for i in range(start_idx, len(fresh) - 1):
            merged = False
            cur_n, cur_N = fresh[i]
            for j in range(i + 1, len(fresh)):
                other_n, other_N = fresh[j]
                if other_n <= cur_N <= other_N or cur_n <= other_n <= cur_N:
                    fresh.pop(i)
                    fresh.insert(i, (min(cur_n, other_n), max(cur_N, other_N)))
                    fresh.pop(j)
                    start_idx = i
                    merged = True
                    break
            if merged:
                break
        if not merged:
            break
    return sum(map(lambda n: n[1] - n[0] + 1, fresh))


if __name__ == '__main__':
    with open('input.txt') as f:
        fresh, ingredients = f.read().split('\n\n')
        fresh = sorted([ tuple(map(int, line.split('-'))) for line in fresh.split() ], key=lambda n: n[0])
        ingredients = { n for n in map(int, ingredients.split()) }

    assert part1(fresh, ingredients) == 623
    assert part2(fresh) == 353507173555373
