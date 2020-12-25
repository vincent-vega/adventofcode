#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def _find_loops(public_keys: list, subject_num: int=7, magic: int=20201227) -> list:
    loop = [ None ] * len(public_keys)
    value, L, missing = 1, 1, len(loop)
    while missing:
        value = value * subject_num % magic
        if value in public_keys:
            loop[public_keys.index(value)] = L
            missing -= 1
        L += 1
    return loop


def _transform(subject_num: int, loop: int, value: int=1, magic: int=20201227) -> int:
    for _ in range(loop):
        value = value * subject_num % magic
    return value


def part1(card_p_key: int, door_p_key: int) -> int:
    card_loops, door_loops = _find_loops([ card_p_key, door_p_key ])
    encryption_key = _transform(card_p_key, door_loops)
    assert encryption_key == _transform(door_p_key, card_loops), "Encryption keys do not match"
    return encryption_key


if __name__ == '__main__':
    with open('input.txt') as f:
        print(part1(*list(map(int, f.read().splitlines()))))  # 6408263
