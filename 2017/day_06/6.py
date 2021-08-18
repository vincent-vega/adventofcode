#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def _reallocate(blocks: list) -> None:
    M = max(blocks)
    block_idx = min(filter(lambda i: blocks[i] == M, range(len(blocks))))
    block_cnt = blocks[block_idx]
    blocks[block_idx] = 0
    cur = (block_idx + 1) % len(blocks)
    while block_cnt > 0:
        blocks[cur] += 1
        block_cnt -= 1
        cur = (cur + 1) % len(blocks)


def _routine(blocks: list) -> (int, int):
    Q = {}
    S = set()
    cycles = 0
    while tuple(blocks) not in S:
        S.add(tuple(blocks))
        Q[tuple(blocks)] = cycles
        _reallocate(blocks)
        cycles += 1
    return cycles, cycles - Q[tuple(blocks)]


def part1(blocks: list) -> int:
    cycles, _ = _routine(list(blocks))
    return cycles


def part2(blocks: list) -> int:
    _, loop_size = _routine(list(blocks))
    return loop_size


if __name__ == '__main__':
    with open('input.txt') as f:
        blocks = list(map(int, ''.join(f.read().splitlines()).split('\t')))
    print(part1(blocks))  # 12841
    print(part2(blocks))  # 8038
