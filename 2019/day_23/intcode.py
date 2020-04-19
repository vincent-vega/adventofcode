class Intcode(object):
    POSITION_MODE  = 0
    IMMEDIATE_MODE = 1
    RELATIVE_MODE  = 2

    @staticmethod
    def _resize(mem, num):
        mem.extend([ 0 for _ in range(num) ])

    @staticmethod
    def _check_resize(mem, addr):
        if addr > len(mem) - 1:
            Intcode._resize(mem, addr - len(mem) + 1)

    @staticmethod
    def _read_value(state, i, m):
        v = state['values']
        base = state['relative_base']
        if m == Intcode.IMMEDIATE_MODE:
            return v[i]
        addr = v[i] if m == Intcode.POSITION_MODE else base + v[i]
        Intcode._check_resize(v, addr)
        return v[addr]

    @staticmethod
    def _write_value(state, i, value, m):
        v = state['values']
        base = state['relative_base']
        assert m == Intcode.POSITION_MODE or m == Intcode.RELATIVE_MODE
        addr = v[i] if m == Intcode.POSITION_MODE else base + v[i]
        Intcode._check_resize(v, addr)
        v[addr] = value

    @staticmethod
    def _add(state, i, m1, m2, m3):
        v1 = Intcode._read_value(state, i + 1, m1)
        v2 = Intcode._read_value(state, i + 2, m2)
        Intcode._write_value(state, i + 3, v1 + v2, m3)
        state['instruction_ptr'] = i + 4
        return state

    @staticmethod
    def _mul(state, i, m1, m2, m3):
        v = state['values']
        v1 = Intcode._read_value(state, i + 1, m1)
        v2 = Intcode._read_value(state, i + 2, m2)
        Intcode._write_value(state, i + 3, v1*v2, m3)
        state['instruction_ptr'] = i + 4
        return state

    @staticmethod
    def _set(state, i, m1, _, __):
        if len(state['input']) == 0:
            state['input_req'] = True
        else:
            Intcode._write_value(state, i + 1, state['input'].popleft(), m1)
            state['instruction_ptr'] = i + 2
        return state

    @staticmethod
    def _out(state, i, m1, _, __):
        val = Intcode._read_value(state, i + 1, m1)
        state['output'].append(val)
        state['instruction_ptr'] = i + 2
        return state

    @staticmethod
    def _jump_true(state, i, m1, m2, _):
        v1 = Intcode._read_value(state, i + 1, m1)
        v2 = Intcode._read_value(state, i + 2, m2)
        state['instruction_ptr'] = v2 if v1 != 0 else i + 3
        return state

    @staticmethod
    def _jump_false(state, i, m1, m2, _):
        v1 = Intcode._read_value(state, i + 1, m1)
        v2 = Intcode._read_value(state, i + 2, m2)
        state['instruction_ptr'] = v2 if v1 == 0 else i + 3
        return state

    @staticmethod
    def _less_than(state, i, m1, m2, m3):
        v1 = Intcode._read_value(state, i + 1, m1)
        v2 = Intcode._read_value(state, i + 2, m2)
        Intcode._write_value(state, i + 3, 1 if v1 < v2 else 0, m3)
        state['instruction_ptr'] = i + 4
        return state

    @staticmethod
    def _equals(state, i, m1, m2, m3):
        v1 = Intcode._read_value(state, i + 1, m1)
        v2 = Intcode._read_value(state, i + 2, m2)
        Intcode._write_value(state, i + 3, 1 if v1 == v2 else 0, m3)
        state['instruction_ptr'] = i + 4
        return state

    @staticmethod
    def _adjust_base(state, i, m1, _, __):
        state['relative_base'] += Intcode._read_value(state, i + 1, m1)
        state['instruction_ptr'] = i + 2
        return state

    @staticmethod
    def _exit(*argv):
        state['exit'] = True
        return state

    @staticmethod
    def _get_opcode(instr):
        return instr%100

    @staticmethod
    def _get_mode(instr):
        return instr//100%10, instr//1000%10, instr//10000

    @staticmethod
    def run_op(state: dict) -> dict:
        instruction_ptr = state['instruction_ptr']
        values = state['values']
        instruction = values[instruction_ptr]
        return {
            1:  Intcode._add,
            2:  Intcode._mul,
            3:  Intcode._set,
            4:  Intcode._out,
            5:  Intcode._jump_true,
            6:  Intcode._jump_false,
            7:  Intcode._less_than,
            8:  Intcode._equals,
            9:  Intcode._adjust_base,
            99: Intcode._exit
        }[Intcode._get_opcode(instruction)](state, instruction_ptr, *Intcode._get_mode(instruction))

