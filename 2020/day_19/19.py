#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Pattern
import regex


def _parse_rule(rule: str) -> str:
    return regex.sub('\s*(\\d+)\s*', '(?&rule\\1)', rule.replace('"', ''))


def _pattern(rules: str) -> str:
    return ''.join([ '(?V1)(?(DEFINE)',
                     ''.join([ f'(?P<rule{n}>{_parse_rule(r)})' for n, r in map(lambda x: x.split(": "), rules.splitlines()) ]),
                     ')^(?&rule0)$' ])


def part1(messages: list, rules: str) -> int:
    pattern: Pattern = regex.compile(_pattern(rules))
    return len([ 1 for m in messages if pattern.match(m) ])


def part2(messages: list, rules: str) -> int:
    rules = rules.replace("8: 42", "8: 42 | 42 8")
    rules = rules.replace("11: 42 31", "11: 42 31 | 42 11 31")
    pattern: Pattern = regex.compile(_pattern(rules))
    return len([ 1 for m in messages if pattern.match(m) ])


if __name__ == '__main__':
    with open('input.txt') as f:
        rules, messages = f.read().split('\n\n')
        messages = messages.strip().split('\n')
    print(part1(messages, rules))  # 265
    print(part2(messages, rules))  # 394
