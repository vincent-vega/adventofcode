import pyperclip
from functools import cache


@cache
def _adj(x: int, y: int) -> list[tuple[int, int]]:
    return [ (x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if abs(dx) != abs(dy) ]


@cache
def _manhattan(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1 - y2)


def _print(s: str):
    pyperclip.copy(s)
    print(s)
