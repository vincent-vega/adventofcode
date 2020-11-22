#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter


def part1(values: list) -> int:
    twos = threes = 0
    for v in values:
        c = Counter(v)
        found_two = found_three = False
        for l, n in c.items():
            if found_two and found_three:
                break
            elif not found_two and n == 2:
                twos += 1
                found_two = True
            elif not found_three and n == 3:
                threes += 1
                found_three = True
    return twos * threes


def part2(values: list) -> str:
    for i in range(0, len(values)):
        current_id = values[i]
        for j in range(i + 1, len(values)):
            diff_count = 0
            diff_char_num = None
            tested_id = values[j]
            for k in range(0, len(current_id)):
                if current_id[k] != tested_id[k]:
                    diff_count += 1
                    diff_char_num = k
                if diff_count > 1:
                    break
            if diff_count == 1:
                return current_id[:diff_char_num] + current_id[(diff_char_num + 1):]


if __name__ == '__main__':
    with open('input.txt') as f:
        values = list(f.read().splitlines())
    print(part1(values))  # 6200
    print(part2(values))  # xpysnnkqrbuhefmcajodplyzw
