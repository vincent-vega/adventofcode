import pyperclip


def _print(s: str):
    pyperclip.copy(s)
    print(s)


def _manhattan(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1 - y2)
