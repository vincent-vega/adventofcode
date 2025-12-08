#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.lib import distance_3d
from itertools import combinations
import heapq


def part1(boxes: list[tuple[int, int, int]], distances: list[tuple[int, int, int]], count: int) -> int:
    box_to_circuit = { }  # dict: box_index -> circuit_idx
    circuits = []  # list of circuits: set[box_indexes]
    for _ in range(count):
        _, idx1, idx2 = heapq.heappop(distances)
        _connect(box_to_circuit, circuits, idx1, idx2)
    *_, one, two, three = sorted([ len(g) for g in circuits if g ])
    return one * two * three


def _connect(box_to_circuit: dict[int, int], circuits: list[set[int]], idx1: int, idx2: int):
    g1 = box_to_circuit.get(idx1, None)
    g2 = box_to_circuit.get(idx2, None)
    if g1 is None and g2 is None:
        g = len(circuits)
        circuits.append({ idx1, idx2 })
        box_to_circuit[idx1] = g
        box_to_circuit[idx2] = g
    elif g1 is None:
        box_to_circuit[idx1] = g2
        circuits[g2].add(idx1)
    elif g2 is None:
        box_to_circuit[idx2] = g1
        circuits[g1].add(idx2)
    elif g1 != g2:
        circuits[g1] |= circuits[g2]
        for b in circuits[g2]:
            box_to_circuit[b] = g1
        circuits[g2] = set()


def part2(boxes: list[tuple[int, int, int]], distances: list[tuple[int, int, int]]) -> int:
    box_to_circuit = { }  # dict box_index -> circuit_idx
    circuits = []  # list of circuits: set[box_indexes]
    while True:
        _, idx1, idx2 = heapq.heappop(distances)
        _connect(box_to_circuit, circuits, idx1, idx2)
        if len(box_to_circuit) == len(boxes):
            for g in filter(lambda g: len(g) > 0, circuits):
                if len(g) == len(boxes):
                    return boxes[idx1][0] * boxes[idx2][0]
                break


if __name__ == '__main__':
    with open('input.txt') as f:
        boxes = list(tuple(map(int, c.split(','))) for c in f.read().splitlines())
    distances = []
    for (idx1, idx2) in combinations(range(len(boxes)), 2):
        b1, b2 = boxes[idx1], boxes[idx2]
        heapq.heappush(distances, (distance_3d(b1, b2), idx1, idx2))
    print(part1(boxes, list(distances), 1000))  # 57970
    print(part2(boxes, distances))  # 8520040659
