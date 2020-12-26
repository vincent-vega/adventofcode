#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re


def _passport(data: list) -> dict:
    return { k: v for k, v in [ d.split(':') for l in data.split('\n') for d in l.split() if ':' in d ] }


def part1(passports: list) -> int:
    return sum([ 1 for p in passports if not { 'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid' } - p.keys() ])


def part2(passports: list) -> int:
    def _is_valid(p: dict) -> bool:
        if { 'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid' } - p.keys():
            return False
        if not re.match('^\\d{4}$', p['byr']) or int(p['byr']) < 1920 or int(p['byr']) > 2002:
            return False
        if not re.match('^\\d{4}$', p['iyr']) or int(p['iyr']) < 2010 or int(p['iyr']) > 2020:
            return False
        if not re.match('^\\d{4}$', p['eyr']) or int(p['eyr']) < 2020 or int(p['eyr']) > 2030:
            return False
        if p['hgt'][-2:] == 'cm' and (int(p['hgt'][:-2]) < 150 or int(p['hgt'][:-2]) > 193):
            return False
        elif p['hgt'][-2:] == 'in' and (int(p['hgt'][:-2]) < 59 or int(p['hgt'][:-2]) > 76):
            return False
        elif p['hgt'][-2:] != 'cm' and p['hgt'][-2:] != 'in':
            return False
        if not re.match('^#[0-9a-f]{6}$', p['hcl']):
            return False
        if p['ecl'] not in { 'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth' }:
            return False
        if not re.match('^\\d{9}$', p['pid']):
            return False
        return True

    return sum([ 1 for p in passports if _is_valid(p) ])


if __name__ == '__main__':
    with open('input.txt') as f:
        passports = [ _passport(p) for p in f.read().split('\n\n') ]
    print(part1(passports))  # 235
    print(part2(passports))  # 194
