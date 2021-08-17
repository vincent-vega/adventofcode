#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter


def part1(passphrases: list) -> int:
    return sum(1 for p in passphrases if len(p) == len(set(p)))


def _chk_anagram(passphrase: list) -> bool:
    words = [ Counter(w) for w in passphrase ]
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            if words[i] == words[j]:
                return False
    return True


def part2(passphrases: list) -> int:
    return sum(1 for p in passphrases if _chk_anagram(p))


if __name__ == '__main__':
    with open('input.txt') as f:
        passphrases = [ l.split() for l in f.read().splitlines() ]
    print(part1(passphrases))  # 451
    print(part2(passphrases))  # 223
