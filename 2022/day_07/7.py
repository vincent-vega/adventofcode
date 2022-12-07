#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Directory:
    def __init__(self, parent, path):
        self.parent = parent
        self.path = path
        self.files = 0
        self.dirs = {}


def _cd(output: list[str], line: int, cur: Directory) -> Directory:
    if line + 1 < len(output):
        if output[line + 1].startswith('$ cd'):
            dir_name = output[line + 1].split()[-1]
            _cd(output, line + 1, cur.parent if dir_name == '..' else cur.dirs[f'{cur.path}/{dir_name}'])
        else:
            _ls(output, line + 2, cur)
    return cur


def _ls(output: list[str], line: int, cur: Directory) -> Directory:
    while line < len(output) and not output[line].startswith('$'):
        size_type, name = output[line].split()
        if size_type == 'dir':
            path = f'{cur.path}/{name}'
            cur.dirs[path] = Directory(cur, path)
        else:
            cur.files += int(size_type)
        line += 1
    if line < len(output):
        nxt_dir = output[line].split()[-1]
        if nxt_dir == '..':
            _cd(output, line, cur.parent)
        else:
            _cd(output, line, cur.dirs[f'{cur.path}/{nxt_dir}'])
    return cur


def _sum(cur: Directory, S: int, max_size: int) -> (int, int):
    cur_size = cur.files
    for d in cur.dirs.values():
        S, child_size = _sum(d, S, max_size)
        cur_size += child_size
    return (S + cur_size, cur_size) if cur_size <= max_size else (S, cur_size)


def part1(root: Directory) -> int:
    return _sum(root, 0, 100_000)[0]


def _du(cur: Directory, size: set) -> int:
    cur_size = cur.files + sum(_du(child, size) for child in cur.dirs.values())
    size.add(cur_size)
    return cur_size


def part2(root: Directory) -> int:
    size = set()
    used = _du(root, size)
    size.add(used)
    return min(filter(lambda n: 70_000_000 - used + n >= 30_000_000, size))


if __name__ == '__main__':
    with open('input.txt') as f:
        root = _cd(f.read().splitlines(), 0, Directory(None, '/'))
    print(part1(root))  # 1513699
    print(part2(root))  # 7991939
