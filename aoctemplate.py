#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests


def part1(values):
    pass


def part2(values):
    pass


def _input(year, day):
    if os.path.isfile('input.txt'):
        return
    url = f'https://adventofcode.com/{year}/day/{day}/input'
    print(f'Downloading input file @ {url}')
    r = requests.get(url, cookies=dict(session=''))
    if r.status_code > 200:
        raise Exception('Unable to download the input file', r.reason)
    with open('input.txt', 'w') as f:
        f.write(r.text)


# import pudb; pu.db
if __name__ == '__main__':
    year, _, day = os.path.realpath(__file__)[:-3].split('/')[-3:]
    _input(year, day)
    with open('input.txt') as f:
        values = list(map(int, f.read().splitlines()))
    print(part1(values))  #
    print(part2(values))  #
