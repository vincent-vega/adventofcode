#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def part1(count: str) -> str:
    recipes = [3, 7]
    elves = (0, 1)
    while len(recipes) < int(count) + 10:
        recipes.extend(map(int, str(recipes[elves[0]] + recipes[elves[1]])))
        elves = tuple((x + 1 + recipes[x]) % len(recipes) for x in elves)
    return ''.join(map(str, recipes[-10:]))


def part2(scores: str) -> int:
    recipes = [3, 7]
    elves = (0, 1)
    match_idx = num_recipes = 0
    while True:
        for c in str(recipes[elves[0]] + recipes[elves[1]]):
            if c == scores[match_idx]:
                match_idx += 1
                if match_idx == 1:
                    num_recipes = len(recipes)
                elif match_idx == len(scores):
                    return num_recipes
            elif match_idx > 0:
                match_idx = 0
            recipes.append(int(c))
        elves = (elves[0] + 1 + recipes[elves[0]]) % len(recipes), (elves[1] + 1 + recipes[elves[1]]) % len(recipes)


if __name__ == '__main__':
    print(part1('236021'))  # 6297310862
    print(part2('236021'))  # 20221334
