INPUT = open('02.txt').read()

# To move 1 unit when facing {direction}, add {x} and {y} to current coordinates
DIRECTION_TO_XY = {
    'U': {'X':  0, 'Y': -1},
    'D': {'X':  0, 'Y': +1},
    'L': {'X': -1, 'Y':  0},
    'R': {'X': +1, 'Y':  0},
}

KEYPAD = (
    '123',
    '456',
    '789',
)

def clamp(v, v_min, v_max):
    # Ensure 0 <= v <= 2
    return min(max(v, v_min), v_max)

def find_code(input):
    # Always start at 5
    x, y = 1, 1
    output = ''
    for line in input.split('\n'):
        # Follow the line instructions
        for direction in line:
            x = clamp(x + DIRECTION_TO_XY[direction]['X'], 0, 2)
            y = clamp(y + DIRECTION_TO_XY[direction]['Y'], 0, 2)

        # Add the digit
        output += KEYPAD[y][x]

    return output


TEST_INPUT = """ULL
RRDDD
LURDL
UUUUD"""
assert find_code(TEST_INPUT) == '1985'
print find_code(INPUT)





KEYPAD2 = (
    '  1  ',
    ' 234 ',
    '56789',
    ' ABC ',
    '  D  ',
)

def find_code2(input):
    # Always start at 5
    x, y = 0, 2
    output = ''
    for line in input.split('\n'):
        # Follow the line instructions
        for direction in line:
            new_x = clamp(x + DIRECTION_TO_XY[direction]['X'], 0, 4)
            new_y = clamp(y + DIRECTION_TO_XY[direction]['Y'], 0, 4)
            # If we're still on a valid key, move to it
            if KEYPAD2[new_y][new_x] != ' ':
                x, y = new_x, new_y

        # Add the digit
        output += KEYPAD2[y][x]

    return output

assert find_code2(TEST_INPUT) == '5DB3'
print find_code2(INPUT)
