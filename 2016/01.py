INPUT = open('01.txt').read()

TURNS = {
    # current -> (left, right)
    'N': {'L': 'W', 'R': 'E'},
    'E': {'L': 'N', 'R': 'S'},
    'S': {'L': 'E', 'R': 'W'},
    'W': {'L': 'S', 'R': 'N'},
}

# To move 1 unit when facing {direction}, add {x} and {y} to current coordinates
DIRECTION_TO_XY = {
    'N': {'X':  0, 'Y': +1},
    'E': {'X': +1, 'Y':  0},
    'S': {'X':  0, 'Y': -1},
    'W': {'X': -1, 'Y':  0},
}

def find_length(instructions):
    current_direction = 'N'
    x = 0
    y = 0
    for instruction in instructions.split(', '):
        # Split the instruction into direction & length
        direction = instruction[0]
        length = int(instruction[1:])

        # Apply the instruction
        current_direction = TURNS[current_direction][direction]
        x += DIRECTION_TO_XY[current_direction]['X'] * length
        y += DIRECTION_TO_XY[current_direction]['Y'] * length
    return abs(x) + abs(y)

assert find_length('R2, L3') == 5
assert find_length('R2, R2, R2') == 2
assert find_length('R5, L5, R5, R3') == 12
print find_length(INPUT)


def find_crossing(instructions):
    current_direction = 'N'
    x = 0
    y = 0
    visited_coords = set()
    for instruction in instructions.split(', '):
        # Split the instruction into direction & length
        direction = instruction[0]
        length = int(instruction[1:])

        # Apply the instruction
        current_direction = TURNS[current_direction][direction]
        dx = DIRECTION_TO_XY[current_direction]['X']
        dy = DIRECTION_TO_XY[current_direction]['Y']
        for i in xrange(length):
            x += dx
            y += dy
            coord = (x, y)
            if coord in visited_coords:
                print coord
                return abs(x) + abs(y)
            visited_coords.add(coord)

assert find_crossing('R8, R4, R4, R8') == 4
print find_crossing(INPUT)
