#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def _react(a: str, b: str) -> bool:
    if ord(a) > ord(b):
        a, b = b, a
    return ord(a) - ord('A') == ord(b) - ord('a')


def _collapse(polymer: str) -> int:
    idx = 0
    result = []
    while idx < len(polymer):
        if idx == len(polymer) - 1:
            if not _react(polymer[idx], result[-1]):
                result.append(polymer[idx])
            else:
                result.pop()
            break
        elif _react(polymer[idx], polymer[idx + 1]):
            idx += 2
            if idx > len(polymer) - 1:
                break
            while result and idx < len(polymer) and _react(polymer[idx], result[-1]):
                result.pop()
                idx += 1
        else:
            assert not _react(polymer[idx], polymer[idx + 1])
            result.append(polymer[idx])
            idx += 1
    return len(result)


def part1(polymer: str) -> int:
    return _collapse(polymer)


def part2(polymer: str) -> int:
    shortest = len(polymer)
    for c in set(polymer.upper()):
        n = _collapse(''.join(p for p in polymer if p not in (c, c.lower())))
        shortest = min(shortest, n)
    return shortest


if __name__ == '__main__':
    with open('input.txt') as f:
        polymer = f.read().strip()
    print(part1(polymer))  # 10564
    print(part2(polymer))  # 6336
