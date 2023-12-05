#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def _c(n: int, mapping: list[tuple[int]]) -> int:
    for dst, src, count in mapping:
        if n >= src and n < src + count:
            return dst + n - src
    return n


def _convert(n: int, soil: list[tuple[int]], fertilizer: list[tuple[int]], water: list[tuple[int]], light: list[tuple[int]], temperature: list[tuple[int]], humidity: list[tuple[int]], location: list[tuple[int]]) -> int:
    return _c(_c(_c(_c(_c(_c(_c(n, soil), fertilizer), water), light), temperature), humidity), location)


def part1(seed: tuple[int], soil: list[tuple[int]], fertilizer: list[tuple[int]], water: list[tuple[int]], light: list[tuple[int]], temperature: list[tuple[int]], humidity: list[tuple[int]], location: list[tuple[int]]) -> int:
    return min(_convert(s, soil, fertilizer, water, light, temperature, humidity, location) for s in seed)


def _is_seed(n: int, seed: list[tuple[int, int]]) -> bool:
    for start, count in seed:
        if n >= start and n < start + count:
            return True
    return False


def _cc(n: int, mapping: list[tuple[int]]) -> int:
    for dst, src, count in mapping:
        if n >= dst and n < dst + count:
            return src + n - dst


def part2(seed: tuple[int], soil: list[tuple[int]], fertilizer: list[tuple[int]], water: list[tuple[int]], light: list[tuple[int]], temperature: list[tuple[int]], humidity: list[tuple[int]], location: list[tuple[int]]) -> int:
    seed = list((seed[i], seed[i + 1]) for i in range(0, len(seed) - 1, 2))
    for dest, src, count in sorted(location, key=lambda x: x[0]):
        for i in range(count):
            n = src + i
            for mapping in (humidity, temperature, light, water, fertilizer, soil):
                if (n := _cc(n, mapping)) is None:
                    break
            else:
                if _is_seed(n, seed):
                    return dest + i


def _mapping(mapping: str) -> list[tuple[int, int, int]]:
    return [ tuple(map(int, m.split())) for m in mapping.splitlines()[1:] ]


if __name__ == '__main__':
    with open('input.txt') as f:
        seed, soil, fertilizer, water, light, temperature, humidity, location = f.read().split('\n\n')
    seed = tuple(map(int, seed.split(': ')[1].split()))
    soil = _mapping(soil)
    fertilizer = _mapping(fertilizer)
    water = _mapping(water)
    light = _mapping(light)
    temperature = _mapping(temperature)
    humidity = _mapping(humidity)
    location = _mapping(location)
    print(part1(seed, soil, fertilizer, water, light, temperature, humidity, location))  # 227653707
    print(part2(seed, soil, fertilizer, water, light, temperature, humidity, location))  # 78775051
