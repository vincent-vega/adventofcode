#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def _nxt(cur: int, depth: int, direction: int) -> (int, int):
    if cur == 0 and direction == -1:
        return 1, 1
    elif cur == depth - 1 and direction == 1:
        return depth - 2, -1
    else:
        return cur + direction, direction


def _move_scanner(firewall: dict) -> dict:
    for k, v in filter(lambda x: x[1] is not None, firewall.items()):
        scanner, depth, direction = v
        scanner, direction = _nxt(scanner, depth, direction)
        firewall[k] = (scanner, depth, direction)
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


def part2(firewall: dict) -> int:
    n = 1
    while _cross(dict(firewall), n) > -1:
        n += 1
    return n


if __name__ == '__main__':
    with open('input.txt') as f:
        layers = { k: v for k, v in map(lambda l: map(int, l.split(': ')), f.read().splitlines()) }
        layers = { 0: 3, 1: 2, 4: 4, 6: 4 }
    firewall = { n: (0, layers[n], 1) if n in layers else None for n in range(max(layers.keys()) + 1) }
    print(part1(firewall))  # 1904
    print(part2(firewall))  #
