#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class FreeSector:
    start: int
    length: int


@dataclass
class File:
    fileid: int
    start: int
    length: int


def part1(disk: dict[int, int], freespace: list[int]) -> int:
    used = [ k for k, v in disk.items() if v is not None ]
    while freespace and used:
        idx = freespace.pop()
        if (cur := used.pop()) < idx:
            break
        disk[idx] = disk[cur]
        disk[cur] = None
    return sum(k * v for k, v in disk.items() if v)


def part2(disk: dict[int, int], files: dict[int, File], free_sectors: list[FreeSector]) -> int:
    for file_id in range(len(files) - 1, -1, -1):
        file = files[file_id]
        for free in free_sectors:
            if free.length >= file.length and free.start < file.start:
                for i in range(file.length):
                    disk[free.start + i] = file.fileid
                    disk[file.start + i] = None
                free.length -= file.length
                free.start += file.length
                break
    return sum(k * v for k, v in disk.items() if v)


if __name__ == '__main__':
    disk = {}
    freespace = []
    free_sectors = []
    files = {}
    with open('input.txt') as f:
        idx = 0
        file_id = 0
        for i, n in enumerate(map(int, f.read().strip())):
            if i % 2 == 0:
                disk.update({ j: file_id for j in range(idx, idx + n) })
                files[file_id] = File(file_id, idx, n)
                file_id += 1
            else:
                freespace.extend(range(idx, idx + n))
                free_sectors.append(FreeSector(idx, n))
            idx += n
    print(part1(dict(disk), freespace[::-1]))  # 6390180901651
    print(part2(disk, files, free_sectors))  # 6412390114238
