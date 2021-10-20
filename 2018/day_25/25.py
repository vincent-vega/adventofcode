#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class DisjointSet:

    def __init__(self, size: int, max_distance: int):
        self.points = []
        self.parent = list(range(size))
        self.rank = [0] * size
        self.constellations = size
        self.max_distance = max_distance


    def add(self, point: tuple):
        j = len(self.points)
        for i in range(len(self.points)):
            if _distance(self.points[i], point) <= self.max_distance:
                self._union(i, j)
        self.points.append(point)
        assert j == self.points.index(point)


    def _find(self, n: int) -> int:
        if self.parent[n] == n:
            return n
        return self._find(self.parent[n])


    def _union(self, p1: int, p2: int):
        p1 = self._find(p1)
        p2 = self._find(p2)
        if p1 == p2:
            return
        if self.rank[p1] < self.rank[p2]:
            self.parent[p1] = p2
        else:
            self.parent[p2] = p1
            if self.rank[p1] == self.rank[p2]:
                self.rank[p1] += 1
        self.constellations -= 1


def _distance(p1: tuple, p2: tuple) -> int:
    return sum(map(lambda x: abs(x[0] - x[1]), zip(p1, p2)))


def part1(points: list) -> int:
    ds = DisjointSet(len(points), 3)
    for p in points:
        ds.add(p)
    return ds.constellations


if __name__ == '__main__':
    with open('input.txt') as f:
        points = [ tuple(map(int, line.split(','))) for line in f.read().splitlines() ]
    print(part1(points))  # 324
