#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import lru_cache


@lru_cache(maxsize=None)
def _nxt(cur: int, depth: int, step: int) -> (int, int):
    if cur == 0 and step == -1:
        return 1, 1
    elif cur == depth - 1 and step == 1:
        return depth - 2, -1
    else:
        return cur + step, step


def _move_scanner(firewall: dict) -> dict:
    for layer, (scanner, depth, step) in filter(lambda x: x[1] is not None, firewall.items()):
        scanner, step = _nxt(scanner, depth, step)
        firewall[layer] = (scanner, depth, step)
    return firewall


def _cross(firewall: dict, wait: int=0) -> int:
    for _ in range(wait):
        firewall = _move_scanner(firewall)
    cnt = -1
    for i in range(len(firewall)):
        if firewall[i] is not None:
            scanner, depth, _ = firewall[i]
            if scanner == 0:
                if cnt == -1:
                    cnt = 0
                cnt += i * depth
        firewall = _move_scanner(firewall)
    return cnt


def part1(firewall: dict) -> int:
    cnt = _cross(dict(firewall))
    return max(cnt, 0)


@lru_cache(maxsize=None)
def _caught(cur: int, depth: int, step: int, delta: int) -> bool:
    for _ in range(delta):
        cur, step = _nxt(cur, depth, step)
    return cur == 0


def part2(firewall: dict) -> int:
    n = 0
    firewall = dict(firewall)
    scanned_levels = [ k for k, _ in filter(lambda x: x[1] is not None, firewall.items()) ]
    while True:
        n += 1
        firewall = _move_scanner(firewall)
        for layer, (cur, depth, step) in map(lambda x: (x, firewall[x]), scanned_levels):
            if _caught(cur, depth, step, layer):
                break
        else:
            return n


if __name__ == '__main__':
    with open('input.txt') as f:
        layers = { k: v for k, v in map(lambda l: map(int, l.split(': ')), f.read().splitlines()) }
    firewall = { n: (0, layers[n], 1) if n in layers else None for n in range(max(layers.keys()) + 1) }
    print(part1(firewall))  # 1904
    print(part2(firewall))  # 3833504
