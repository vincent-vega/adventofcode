#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def trim_dict_map(d_map: dict) -> dict:
    X, _ = max(d_map, key=lambda k: k[0])
    _, Y = max(d_map, key=lambda k: k[1])
    return { (x, y): True for x, y in d_map if x > 0 and x < X and y > 0 and y < Y }


def rotate_dict_map_90(d_map: dict) -> dict:
    _, Y = max(d_map, key=lambda k: k[1])
    return { (Y - y, x): True for x, y in d_map }


def flip_dict_map_X(d_map: dict) -> dict:
    _, Y = max(d_map, key=lambda k: k[1])
    return { (x, Y - y): True for x, y in d_map }


def flip_dict_map_Y(d_map: dict) -> dict:
    X, _ = max(d_map, key=lambda k: k[0])
    return { (X - x, y): True for x, y in d_map }


def inverted(border: tuple) -> tuple:
    return tuple(9 - x for x in border[::-1])


def flip_X(puzzle: dict, border: dict, tile_num: int, flip_puzzle=False):
    if flip_puzzle:
        top, right, bottom, left = puzzle[tile_num]
        puzzle[tile_num] = [ bottom, right, top, left ]
    top, right, bottom, left = border[tile_num]
    border[tile_num] = [ bottom, inverted(right), top, inverted(left) ]


def flip_Y(puzzle: dict, border: dict, tile_num: int, flip_puzzle=False):
    if flip_puzzle:
        top, right, bottom, left = puzzle[tile_num]
        puzzle[tile_num] = [ top, left, bottom, right ]
    top, right, bottom, left = border[tile_num]
    border[tile_num] = [ inverted(top), left, inverted(bottom), right ]


def rotate_90(puzzle: dict, border: dict, tile_num: int, times: int=1, rotate_puzzle=False):
    for _ in range(times % 4):
        if rotate_puzzle:
            top, right, bottom, left = puzzle[tile_num]
            puzzle[tile_num] = [ left, top, right, bottom ]
        top, right, bottom, left = border[tile_num]
        border[tile_num] = [ inverted(left), top, inverted(right), bottom ]


def parse_border_Y(tile: dict, up: bool) -> tuple:
    _, Y = max(tile, key=lambda k: k[1])
    return tuple(sorted([ x for x, y in tile if y == 0 ])) if up else tuple(sorted([ x for x, y in tile if y == Y ]))


def parse_border_X(tile: dict, right: bool) -> tuple:
    X, _ = max(tile, key=lambda k: k[0])
    return tuple(sorted([ y for x, y in tile if x == X ])) if right else tuple(sorted([ y for x, y in tile if x == 0 ]))


def swap(puzzle: dict, t1: int, t1_idx: int, t2: int, t2_idx: int):
    if puzzle[t1][t1_idx] != t2:
        i = puzzle[t1].index(t2)
        puzzle[t1][t1_idx], puzzle[t1][i] = puzzle[t1][i], puzzle[t1][t1_idx]
    if puzzle[t2][t2_idx] != t1:
        i = puzzle[t2].index(t1)
        puzzle[t2][t2_idx], puzzle[t2][i] = puzzle[t2][i], puzzle[t2][t2_idx]


def _line(tile: dict, line: int) -> str:
    return ''.join([ '#' if (x, line) in tile else '.' for x in range(1, 9) ])


def _lines(tiles: list):
    return [ ''.join([ _line(t, line) for t in tiles ]) for line in range(1, 9) ]


def _lines_ids(puzzle: dict) -> list:
    top_left = [ n for n, (top, right, bottom, left) in puzzle.items() if top is None and left is None ]
    assert len(top_left) == 1, 'Multiple top left corners found'
    top_left = top_left.pop()
    lines = [ [ top_left ] ]
    *_, cur, __ = puzzle[top_left]
    while cur is not None:
        lines.append([ cur ])
        *_, cur, __ = puzzle[cur]
    for l in lines:
        first = l[0]
        _, cur, *__ = puzzle[first]
        while cur is not None:
            l.append(cur)
            _, cur, *__ = puzzle[cur]
    return lines


def tiles_ascii(tiles: dict, puzzle: dict) -> list:
    return [ l for line in _lines_ids(puzzle) for l in _lines([ tiles[t] for t in line ]) ]


def worlddict(map_lines: list) -> dict:
    return { (x, y): True for y in range(len(map_lines)) for x in range(len(map_lines[y])) if map_lines[y][x] == '#' }
