#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from collections import defaultdict


def part1(instructions: dict) -> str:
    letters = { k for k in instructions }
    letters.update(v for value in instructions.values() for v in value)
    ready = letters - instructions.keys()
    steps = list(sorted(ready)[0])
    ready.remove(steps[0])
    remaining = letters - set(steps)
    while remaining:
        for after in remaining:
            if all(before in steps for before in instructions[after]):
                ready.add(after)
        steps.append(sorted(ready)[0])
        ready.remove(steps[-1])
        remaining.remove(steps[-1])
    return ''.join(steps)


def _task_duration(task: str, delta: int) -> int:
    return delta + ord(task) - ord('A') + 1


def part2(instructions: dict, num_workers: int, delta: int) -> int:
    letters = { k for k in instructions }
    letters.update(v for value in instructions.values() for v in value)
    available = sorted(letters - instructions.keys(), reverse=True)
    done = set()
    remaining = set(letters)
    workers = [ None ] * num_workers
    time = -1
    while remaining:
        time += 1
        for n, w in ((n, w) for n, w in enumerate(workers) if w and w[1] == 1):
            task, _ = w
            done.add(task)
            remaining.remove(task)
            workers[n] = None
        for after in letters - done - { task for task, _ in filter(lambda w: w, workers) } - set(available):
            if all(before in done for before in instructions[after]):
                available.append(after)
        available = sorted(available, reverse=True)
        for n, w in enumerate(workers):
            if w is None and available:
                task = available.pop()
                workers[n] = (task, _task_duration(task, delta))
            elif w:
                task, task_time = w
                workers[n] = (task, task_time - 1)
    return time


if __name__ == '__main__':
    with open('input.txt') as f:
        instructions = defaultdict(set)
        for line in f.read().splitlines():
            before, after = re.findall(r'\b[A-Z]\b', line)
            instructions[after].add(before)
    print(part1(instructions))  # MNQKRSFWGXPZJCOTVYEBLAHIUD
    print(part2(instructions, 5, 60))  # 948
