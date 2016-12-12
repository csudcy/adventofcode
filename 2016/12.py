INPUT = open('12.txt').read().strip()

import time


def compile_line(line):
    # Parse a line into
    # (instruction, [args...])
    parts = line.split()
    return parts[0], parts[1:]


def compile(input):
    return [
        compile_line(line)
        for line in input.split('\n')
    ]


def execute(program, a=0, b=0, c=0, d=0):
    registers = {
        'a': a,
        'b': b,
        'c': c,
        'd': d,
    }

    def get_register_or_value(key):
        if key in registers:
            return registers[key]
        return int(key)

    pc = 0
    iters = 0
    start_time = time.time()
    next_time = time.time()
    while pc < len(program):
        instruction, args = program[pc]
        if instruction == 'cpy':
            registers[args[1]] = get_register_or_value(args[0])
        elif instruction == 'inc':
            registers[args[0]] += 1
        elif instruction == 'dec':
            registers[args[0]] -= 1
        elif instruction == 'jnz':
            if get_register_or_value(args[0]) != 0:
                # Execute the jump (-1 cause that will be added later)
                pc += int(args[1]) - 1
        else:
            raise Exception('Unknown instruction: ' + instruction[0])
        pc += 1
        iters += 1

        if time.time() > next_time:
            diff_time = time.time() - start_time
            print '{diff_time:.02f}s : {iters} iters, a: {registers[a]}'.format(
                diff_time=diff_time,
                iters=iters,
                registers=registers,
            )
            next_time = time.time() + 1

    return registers


TEST_INPUT = """cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a"""
test_program = compile(TEST_INPUT)
print test_program
test_registers = execute(test_program)
assert test_registers['a'] == 42


program = compile(INPUT)
registers = execute(program)
print registers

registers = execute(program, c=1)
print registers
