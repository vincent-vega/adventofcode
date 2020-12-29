#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tilesmanipulation import tiles_ascii, worlddict, inverted, rotate_90, \
    flip_X, flip_Y, rotate_dict_map_90, flip_dict_map_X, swap, \
    flip_dict_map_Y, parse_border_X, parse_border_Y, trim_dict_map
from functools import reduce
import re


def _count_hashtags(world: dict, monsters: list) -> int:
    skip = { coord for m in monsters for coord in _monster_vertex(m) }
    return sum(1 for coord in world if coord not in skip)


def _monster_vertex(coord: (int, int)) -> list:
    x, y = coord
    return [ (x + dx, y + dy) for dx, dy in _monster_vertex_delta() ]


def _monster_vertex_delta() -> list:
    return [ (18, 0), (0, 1), (5, 1), (6, 1), (11, 1), (12, 1), (17, 1),
             (18, 1), (19, 1), (1, 2), (4, 2), (7, 2), (10, 2), (13, 2),
             (16, 2) ]


def _find_monsters(world: dict) -> list:
    """
    Return the list of top-left vertexes corresponding to the monsters
    found in the map.
    """
    X, _ = max(world, key=lambda k: k[0])
    _, Y = max(world, key=lambda k: k[1])
    return [ (x, y) for y in range(Y - 2) for x in range(X - 18) if _monster_present(world, (x, y)) ]


def _monster_present(world: dict, top_left_coord: (int, int)) -> bool:
    return all((x, y) in world for x, y in _monster_vertex(top_left_coord))


def _get_connections(border: dict) -> dict:
    puzzle = { n: [] for n in border }
    for tile_num in border:
        curr_bor_set = set(border[tile_num])
        for n, bb in filter(lambda x: x[0] != tile_num, border.items()):
            if len(curr_bor_set & set(bb)) > 0 or len(curr_bor_set & { inverted(b) for b in bb }) > 0:
                puzzle[tile_num].append(n)
        for _ in range(len(puzzle[tile_num]), 4):
            puzzle[tile_num].append(None)
    return puzzle


def _rearrange(tiles: dict, border: dict, puzzle: dict):
    # PUZZLE/BORDER 0: up, 1: right, 2: bottom, 3: left
    first_tile_num = list(puzzle.keys())[0]
    seen = set([ first_tile_num ])
    to_arrange = [ t for t in puzzle[first_tile_num] if t is not None ]
    while to_arrange:
        cur = to_arrange.pop(0)  # current tile number
        to_arrange.extend([ t for t in puzzle[cur] if t not in seen and t is not None and t not in to_arrange ])
        to_connect = [ t for t in puzzle[cur] if t in seen ]  # tile numbers to connect with
        connected = False  # if True, the current tile has been connected with at least another tile
        for other in to_connect:
            bord = (set(border[cur]) | set([ inverted(b) for b in border[cur] ])) & set(border[other])
            assert len(bord) == 1, 'Multiple match'
            bord = bord.pop()
            other_idx = border[other].index(bord)
            cur_idx = (other_idx + 2) % 4
            if not connected:
                while border[cur][cur_idx] not in { bord, inverted(bord) }:
                    rotate_90(puzzle, border, cur)
                    tiles[cur] = rotate_dict_map_90(tiles[cur])
                assert border[other][other_idx] == border[cur][cur_idx] or border[other][other_idx] == inverted(border[cur][cur_idx]), 'Connected boarders do not match'
                if bord == inverted(border[cur][cur_idx]):
                    if cur_idx == 0 or cur_idx == 2:
                        flip_Y(puzzle, border, cur)
                        tiles[cur] = flip_dict_map_Y(tiles[cur])
                    else:
                        flip_X(puzzle, border, cur)
                        tiles[cur] = flip_dict_map_X(tiles[cur])
                swap(puzzle, cur, cur_idx, other, other_idx)
            else:
                if border[cur][cur_idx] != border[other][other_idx]:
                    assert border[cur][cur_idx] == inverted(border[other][other_idx]), 'Connected boarders cannot match'
                    if cur_idx == 0 or cur_idx == 2:
                        flip_Y(puzzle, border, cur)
                        tiles[cur] = flip_dict_map_Y(tiles[cur])
                    else:
                        flip_X(puzzle, border, cur)
                        tiles[cur] = flip_dict_map_X(tiles[cur])
                swap(puzzle, cur, cur_idx, other, other_idx)
            connected = True
        seen.add(cur)  # the current tile has been connected and won't be moved again


def part1(tiles: dict) -> int:
    border = { n: [ parse_border_Y(t, True), parse_border_X(t, True), parse_border_Y(t, False), parse_border_X(t, False) ] for n, t in tiles.items() }

    def _count_match(tile_border: tuple, others: tuple) -> int:
        return len([ 1 for b in tile_border if b in others or inverted(b) in others ])
    return reduce(lambda a, b: a * b, [ n for n, b in border.items() if _count_match(b, { b for nn, bb in border.items() for b in bb if n != nn }) == 2 ])


def part2(tiles: dict) -> int:
    border = { n: [ parse_border_Y(t, True), parse_border_X(t, True), parse_border_Y(t, False), parse_border_X(t, False) ] for n, t in tiles.items() }
    puzzle = _get_connections(border)
    _rearrange(tiles, border, puzzle)
    world = worlddict(tiles_ascii({ n: trim_dict_map(t) for n, t in tiles.items() }, puzzle))
    for _ in range(2):
        for _ in range(4):
            monsters = _find_monsters(world)
            if not monsters:
                world = rotate_dict_map_90(world)
                continue
            return _count_hashtags(world, monsters)
        world = flip_dict_map_Y(world)
    raise Exception('No monsters found')


if __name__ == '__main__':
    tiles = {}
    with open('input.txt') as f:
        for tile in f.read().strip().split('\n\n'):
            num, tile = tile.split(':\n')
            num = list(map(int, re.findall('\\d+', num))).pop()
            tiles[num] = { (x, y): True for y, line in enumerate(tile.split('\n')) for x, c in enumerate(line) if c == '#' }
    print(part1(tiles))  # 18411576553343
    print(part2(tiles))  # 2002
