#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re


def part1(rules: dict, what: str) -> int:
    """
        rules: {
            (content1, content2, ...): [container1, container2, ...],
            ...
        }
    """
    target, next_target, seen = set([ what ]), set(), set([ what ])
    count = 0
    while target:
        for key in rules.keys():
            for _ in range(len(target & set(key))):
                containers = [ c for c in rules[key] if c not in seen ]
                count += len(containers)
                next_target.update(containers)
                seen.update(containers)
        target, next_target = next_target, set()
    return count


def part2(rules: dict, what: str) -> int:
    """
        rules: {
            container: [(quantity1, content1), (quantity2, content2), ...],
            ...
        }
    """
    target = list(rules[ what ])
    count = 0
    while target:
        q, w = target.pop()
        count += int(q)
        target.extend([ (qq, ww) for _ in range(int(q)) for qq, ww in rules[w] ])
    return count


if __name__ == '__main__':
    with open('input.txt') as f:
        R = {}
        for l in f.read().splitlines():
            container, content = l.split(' bags contain ')
            if container != 'shiny gold' and content != 'no other bags.':
                content = tuple([ re.sub('(bags?|\\.|\\d)', '', chunk).strip() for chunk in content.split(', ') ])
                R[content] = [ container ] + R[content] if content in R else [ container ]
    print(part1(R, 'shiny gold'))  # 208

    with open('input.txt') as f:
        R = {}
        for l in f.read().splitlines():
            container, content = l.split(' bags contain ')
            if content == 'no other bags.':
                content = []
            else:
                content = content[:-1].split(', ')
                content = [ tuple(re.sub(' bags?', '', c).split(' ', 1)) for c in content ]
            R[container] = content
    print(part2(R, 'shiny gold'))  # 1664
