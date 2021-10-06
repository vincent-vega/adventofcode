#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter, defaultdict, namedtuple
import re

Record = namedtuple('Record', [ 'year', 'month', 'day', 'hour', 'minute', 'guard', 'sleep', 'wakeup' ])


def _parse_record(line: str) -> Record:
    try:
        return Record(*map(int, re.findall(r'\d+', line)), False, False)
    except TypeError:
        return Record(*map(int, re.findall(r'\d+', line)), None, 'asleep' in line, 'wakes' in line)


def _summarize(records: list) -> dict:
    summary = defaultdict(list)
    cur_guard = start = None
    for r in records:
        if r.guard:
            cur_guard = r.guard
        elif r.sleep:
            start = r.minute
        elif r.wakeup:
            summary[cur_guard].extend(m for m in range(start, r.minute))
    return summary


def part1(records: list) -> int:
    summary = _summarize(records)
    guard = max(summary.keys(), key=lambda k: len(summary[k]))
    minutes = Counter(summary[guard])
    return guard * max(minutes.keys(), key=lambda k: minutes[k])


def part2(records: list) -> int:
    summary = _summarize(records)
    guard = minute = cnt = -1
    for g, t in summary.items():
        c = Counter(t)
        k = max(c.keys(), key=lambda k: c[k])
        if c[k] > cnt:
            guard = g
            minute = k
            cnt = c[k]
    return guard * minute


if __name__ == '__main__':
    with open('input.txt') as f:
        records = sorted(map(_parse_record, f.read().splitlines()), key=lambda r: (r.year, r.month, r.day, r.hour, r.minute))
    print(part1(records))  # 151754
    print(part2(records))  # 19896
