#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce
from typing import Type


class Packet:
    def __init__(self, version: int, packet_type: int):
        self.version = version
        self.packet_type = packet_type
        self.sub = []

    def set(self, n: int):
        self.v = n

    def addsub(self, packet):
        self.sub.append(packet)

    def versionsum(self) -> int:
        return self.version + sum(p.versionsum() for p in self.sub)

    def _sum(self) -> int:
        if not self.sub:
            return self.value()
        return sum(p.value() for p in self.sub)

    def _mul(self) -> int:
        if not self.sub:
            return self.value()
        return reduce(lambda a, b: a * b, (p.value() for p in self.sub))

    def _min(self) -> int:
        if not self.sub:
            return self.value()
        return min(p.value() for p in self.sub)

    def _max(self) -> int:
        if not self.sub:
            return self.value()
        return max(p.value() for p in self.sub)

    def _gt(self) -> int:
        return 1 if self.sub[0].value() > self.sub[1].value() else 0

    def _lt(self) -> int:
        return 1 if self.sub[0].value() < self.sub[1].value() else 0

    def _eq(self) -> int:
        return 1 if self.sub[0].value() == self.sub[1].value() else 0

    def value(self) -> int:
        T = self.packet_type
        return self.v if T == 4 else { 0: self._sum,
                                       1: self._mul,
                                       2: self._min,
                                       3: self._max,
                                       5: self._gt,
                                       6: self._lt,
                                       7: self._eq }[T]()


def _header(transmission: str, idx: int) -> (int, int):
    return int(transmission[idx:idx + 3], 2), int(transmission[idx + 3:idx + 6], 2)


def _literal(transmission: str, idx: int) -> (int, Type[Packet]):
    packet = Packet(*_header(transmission, idx))
    idx += 6
    value = []
    while transmission[idx] != '0':
        value.append(transmission[idx + 1:idx + 5])
        idx += 5
    value.append(transmission[idx + 1:idx + 5])
    packet.set(int(''.join(value), 2))
    return idx + 5, packet


def _operator(transmission: str, idx: int) -> (int, Type[Packet]):
    packet = Packet(*_header(transmission, idx))
    idx += 6
    length_type_id = int(transmission[idx], 2)
    lengthbits = 15 if length_type_id == 0 else 11
    idx += 1
    length = int(transmission[idx:idx + lengthbits], 2)
    idx += lengthbits
    start = idx
    if length_type_id == 0:
        while idx - start < length:
            idx, p = _parse(transmission, idx)
            packet.addsub(p)
    else:
        for _ in range(length):
            idx, p = _parse(transmission, idx)
            packet.addsub(p)
    return idx, packet


def _parse(transmission: str, idx: int) -> (int, Type[Packet]):
    T = int(transmission[idx + 3:idx + 6], 2)
    return _literal(transmission, idx) if T == 4 else _operator(transmission, idx)


def part1(transmission: str) -> int:
    _, packet = _parse(transmission, 0)
    return packet.versionsum()


def part2(transmission: str) -> int:
    _, packet = _parse(transmission, 0)
    return packet.value()


if __name__ == '__main__':
    with open('input.txt') as f:
        transmission = ''.join(bin(int(h, 16))[2:].zfill(4) for h in f.read().strip())
    print(part1(transmission))  # 893
    print(part2(transmission))  # 4358595186090
