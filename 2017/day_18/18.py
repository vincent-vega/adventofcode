#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Program:
    def __init__(self, n: int, instructions: list):
        self.cnt = self.cur = 0
        self.instructions = instructions
        self.rcv = []
        self.snd = []
        self.registers = { k: n if k == 'p' else 0 for k, v in _init().items() }


    def run(self) -> int:
        while self.cur > -1 and self.cur < len(self.instructions):
            i = instructions[self.cur]
            if i[0] == 'jgz' and _value(self.registers, i[1]) > 0:
                self.cur += _value(self.registers, i[2])
                continue
            elif i[0] == 'snd':
                self.snd.append(self.registers[i[1]])
                self.cnt += 1
            elif i[0] == 'rcv':
                if not self.rcv:
                    return 1
                self.registers[i[1]] = self.rcv.pop(0)
            else:
                _run_op(self.registers, i)
            self.cur += 1
        return 0


def _init() -> dict:
    return { chr(ord('a') + n): 0 for n in range(ord('z') - ord('a')) }


def _value(registers: dict, parameter: str) -> int:
    return registers[parameter] if parameter in registers else int(parameter)


def _run_op(registers: dict, instruction: tuple) -> None:
    op, p1, p2 = instruction
    if op == 'set':
        registers[p1] = _value(registers, p2)
    elif op == 'add':
        registers[p1] += _value(registers, p2)
    elif op == 'mul':
        registers[p1] *= _value(registers, p2)
    elif op == 'mod':
        registers[p1] %= _value(registers, p2)


def part1(instructions: list) -> int:
    registers = _init()
    cur = 0
    last = None
    while cur > -1 and cur < len(instructions):
        i = instructions[cur]
        if i[0] == 'jgz' and _value(registers, i[1]) > 0:
            cur += _value(registers, i[2])
            continue
        elif i[0] == 'snd':
            last = registers[i[1]]
        elif i[0] == 'rcv' and registers[i[1]] > 0:
            break
        else:
            _run_op(registers, i)
        cur += 1
    return last


def part2(instructions: list) -> int:
    P0, P1 = Program(0, instructions), Program(1, instructions)
    p0 = P0.run()
    p1 = P1.run()
    while p0 and P1.snd or p1 and P0.snd:
        P0.rcv += [ P1.snd.pop(0) for _ in range(len(P1.snd)) ]
        P1.rcv += [ P0.snd.pop(0) for _ in range(len(P0.snd)) ]
        p0 = P0.run()
        p1 = P1.run()
    return P1.cnt


if __name__ == '__main__':
    with open('input.txt') as f:
        instructions = [ tuple(l.split()) for l in f.read().splitlines() ]
    print(part1(instructions))  # 7071
    print(part2(instructions))  # 8001
