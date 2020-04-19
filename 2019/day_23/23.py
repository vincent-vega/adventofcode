#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque
from intcode import Intcode
from multiprocessing import Process, Manager

def _main1(address: int, mailbox: dict, values: list):
    assert address in mailbox
    state = {
        'values': values,
        'instruction_ptr': 0,
        'exit': False,
        'output': deque(),
        'input': deque([ address ]),
        'input_req': False,
        'relative_base': 0
    }
    while not state['exit'] and len(mailbox[255]) == 0:
        state = Intcode.run_op(state)
        if state['input_req']:
            state['input_req'] = False
            if len(mailbox[address]) > 0:
                x, y = mailbox[address].pop(0)
                state['input'].extend([ x, y ])
            else:
                state['input'].append(-1)
        while len(state['output']) > 2 :
            addr = state['output'].popleft()
            x = state['output'].popleft()
            y = state['output'].popleft()
            mailbox[addr].append((x, y))

def _init(mgr: Manager) -> dict:
    d = mgr.dict()
    for i in range(50):
        d[i] = mgr.list()
    d[255] = mgr.list()
    return d

def part1(values: list) -> int:
    with Manager() as manager:
        p_list = []
        d = _init(manager)
        for i in range(50):
            p = Process(target=_main1, args=(i, d, list(values)))
            p_list.append(p)
            p.start()
        for p in p_list:
            p.join()
        x, y = d[255].pop(0)
        return y

def _nat(address: int, mailbox: dict, values: list):
    assert address in mailbox
    packet_mem = None
    while True: # TODO
        # lock mailbox
        # get messages
        # release mailbox
        # check idle
        # send packet
        # wait with timeout
        while len(mailbox[address]) > 0:
            x, y = mailbox[address].pop(0)
            if packet_mem is not None and packet_mem == (x, y):
                # TODO
                pass

def _main2(address: int, mailbox: dict, values: list):
    assert address in mailbox
    state = {
        'values': values,
        'instruction_ptr': 0,
        'exit': False,
        'output': deque(),
        'input': deque([ address ]),
        'input_req': False,
        'relative_base': 0
    }
    while not state['exit']: # TODO
        state = _run_op(state)
        if state['input_req']:
            state['input_req'] = False
            if len(mailbox[address]) > 0:
                x, y = mailbox[address].pop(0)
                state['input'].extend([ x, y ])
            else:
                state['input'].append(-1)
        while len(state['output']) > 2 :
            addr = state['output'].popleft()
            x = state['output'].popleft()
            y = state['output'].popleft()
            mailbox[addr].append((x, y))

def part2(values: list) -> int:
    with Manager() as manager:
        p_list = []
        d = _init(manager)
        for i in range(50):
            p = Process(target=_main2, args=(i, d, list(values)))
            p_list.append(p)
            p.start()
        nat = Process(target=_nat, args=(255, d, list(values)))
        nat.start()
        for p in p_list:
            p.join()
        nat.join()

if __name__ == '__main__':
    with open('input.txt') as f:
        values = list(map(int, f.read().split(',')))
    print(part1(values)) # 23815
    #print(part2(values)) #

