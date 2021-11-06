#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def _match_rule(pots: set, pot_num: int, rule: tuple) -> bool:
    for idx in range(-2, 3):
        if idx in rule and pot_num + idx not in pots:
            return False
        elif idx not in rule and pot_num + idx in pots:
            return False
    return True


def _is_plant(pots: set, rules: dict, pot_num: int) -> bool:
    for rule, outcome in rules.items():
        if _match_rule(pots, pot_num, rule):
            return outcome
    raise Exception('No match!')


def _next_gen(pots: set) -> set:
    return { n for n in range(min(pots) - 2, max(pots) + 3) if _is_plant(pots, rules, n) }


def part1(pots: set, rules: dict) -> int:
    for _ in range(20):
        pots = _next_gen(pots)
    return sum(pots)


def part2(pots: set, rules: dict) -> int:
    same_diff_iteration_count = 0
    sums = [ sum(pots) ]
    prev_diff = sum(pots)
    while same_diff_iteration_count < 500:
        pots = _next_gen(pots)
        s = sum(pots)
        d = s - sums[-1]
        if d == prev_diff:
            same_diff_iteration_count += 1
        else:
            same_diff_iteration_count = 0
            prev_diff = d
        sums.append(s)
    # for 500 iterations, the pots count increment has been the same
    return sums[-500] + prev_diff * (50_000_000_000 - len(sums) + 500)


if __name__ == '__main__':
    with open('input.txt') as f:
        pots = { n for n, c in enumerate(f.readline()[len('initial state: '):]) if c == '#' }
        rules = { tuple(n for n, c in enumerate(k, -2) if c == '#'): v == '#' for k, v in map(lambda line: line.split(' => '), filter(len, f.read().splitlines())) }
    print(part1(pots, rules))  # 3410
    print(part2(pots, rules))  # 4000000001480
