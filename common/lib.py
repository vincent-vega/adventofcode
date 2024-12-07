import pyperclip


def _print(s: str):
    pyperclip.copy(s)
    print(s)
