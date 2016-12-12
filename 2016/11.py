"""
Initial setup:

1=polonium
2=thulium
3=promethium
4=ruthenium
5=cobalt

     1  2  3  4  5
F4
F3
F2    M     M
F1 E G  GM G  GM GM
"""

# NOTE: I've tried to use index to indicate 0 based and number to indicate 1 based

# Movement directions
U = 1
D = -1
# Indexes in the isotope array
G = 0
M = 1

ELEVATOR_FLOOR = 0
ISOTOPES = 1


import copy


def init_state(*isotopes):
    # isotopes is a list of (name, generator floor, microchip floor)
    return (
        # Elevator floor index
        0,
        # Isotopes (gen_floor_index, chip_floor_index)
        [
            [isotope[1] - 1, isotope[2] - 1]
            for index, isotope in enumerate(isotopes)
        ],
    )


def move_state(state, direction, *items):
    # items is a list of (isotope_index, gen_or_chip)

    # Have to have an item to use the lift
    if len(items) == 0:
        raise Exception('You cannot use the lift without taking an item!')

    # Have to be moving to a valid floor
    new_floor_index = get_new_floor_or_none(state, direction)
    if new_floor_index is None:
        raise Exception(
            'You cannot move {direction} floor from floor index {floor_index}!'.format(
                direction=direction,
                floor_index=state[ELEVATOR_FLOOR]
            )
        )

    # Check all items are on the same floor as the elevator
    for isotope_index, gen_or_chip in items:
        if not can_pickup(state, isotope_index, gen_or_chip):
            raise Exception(
                'Isotope index {isotope_index} {gen_or_chip} is on floor index {floor_index}; you cannot pick it up in the elevator on floor index {elevator_floor_index}!'.format(
                    isotope_index=isotope_index,
                    gen_or_chip='gen' if gen_or_chip == G else 'chip',
                    floor_index=state[ISOTOPES][isotope_index][gen_or_chip],
                    elevator_floor_index=state[ELEVATOR_FLOOR]
                )
            )

    # Move to the new floor / make the new state
    new_state = (
        new_floor_index,
        # OH MY GOD, THIS SUCKS!
        copy.deepcopy(state[ISOTOPES])
    )
    for isotope_index, gen_or_chip in items:
        new_state[ISOTOPES][isotope_index][gen_or_chip] = new_floor_index

    # Check no chips have died
    toasted_chip_indexes = get_toasted_chip_indexes(new_state)
    if toasted_chip_indexes:
        raise Exception(
            'You have toasted these chips: {toasted_chip_indexes}'.format(
                toasted_chip_indexes=toasted_chip_indexes,
            )
        )

    return new_state


def get_new_floor_or_none(state, direction):
    new_floor_index = state[ELEVATOR_FLOOR] + direction
    if new_floor_index < 0 or new_floor_index >= 4:
        return None
    return new_floor_index


def can_pickup(state, isotope_index, gen_or_chip):
    floor_index = state[ISOTOPES][isotope_index][gen_or_chip]
    return floor_index == state[ELEVATOR_FLOOR]


def get_floors_have_generators(state):
    floors_have_generators = [False] * 4
    for isotope in state[ISOTOPES]:
        floors_have_generators[isotope[G]] = True
    return floors_have_generators


def get_toasted_chip_indexes(state):
    floors_have_generators = get_floors_have_generators(state)
    toasted_chip_indexes = []
    for index, isotope in enumerate(state[ISOTOPES]):
        # This chip is with it's generator; it is safe
        if isotope[G] == isotope[M]:
            continue
        # If there are any generators on this chip's floor, the chip is toast
        if floors_have_generators[isotope[M]]:
            toasted_chip_indexes.append(index)

    return toasted_chip_indexes


def is_complete(state):
    for isotope in state[ISOTOPES]:
        if isotope[M] != 3 or isotope[G] != 3:
            return False
    return True


def output(state):
    # Output in a semi-nice way
    output = []

    # Add the isotope header
    output.append(
        '     ' + '  '.join(
            map(str, xrange(len(state[ISOTOPES])))
        )
    )

    # Add the floors
    floors_output = []
    for floor_index in xrange(4):
        floor_output = [
            # Add the floor identifier
            'F' + str(floor_index+1),
            # Add if the elevator is here
            'E' if state[ELEVATOR_FLOOR] == floor_index else ' '
        ]
        for isotope in state[ISOTOPES]:
            floor_output.append(
                ('G' if isotope[G] == floor_index else ' ') +
                ('M' if isotope[M] == floor_index else ' ')
            )
        floors_output.append(' '.join(floor_output))

    output += reversed(floors_output)

    return '\n'.join([
        line.rstrip()
        for line in output
    ])


def solve(state):
    """
    From state, use a breadth first search to find the shortest path to a solution
    """
    pass




EXPECTED_TEST_OUTPUT = """     0  1
F4
F3      G
F2   G
F1 E  M  M"""

TEST_SETUP = [
    ('Hydrogen', 2, 1),
    ('Lithium', 3, 1),
]
TEST_BUILDING = init_state(*TEST_SETUP)
assert TEST_BUILDING == (0, [[1, 0], [2, 0]])
print output(TEST_BUILDING)
assert output(TEST_BUILDING) == EXPECTED_TEST_OUTPUT
assert get_new_floor_or_none(TEST_BUILDING, 0) == 0
assert get_new_floor_or_none(TEST_BUILDING, 1) == 1
assert get_new_floor_or_none(TEST_BUILDING, 3) == 3
assert get_new_floor_or_none(TEST_BUILDING, -1) == None
assert get_new_floor_or_none(TEST_BUILDING, 4) == None
assert can_pickup(TEST_BUILDING, 0, M) == True
assert can_pickup(TEST_BUILDING, 0, G) == False
assert can_pickup(TEST_BUILDING, 1, M) == True
assert can_pickup(TEST_BUILDING, 1, G) == False
assert get_floors_have_generators(TEST_BUILDING) == [False, True, True, False]
assert get_toasted_chip_indexes(TEST_BUILDING) == []
assert is_complete(TEST_BUILDING) == False




# Both chips should be toast
BAD_TEST_SETUP = [
    ('Hydrogen', 2, 1),
    ('Lithium', 1, 2),
]
BAD_TEST_BUILDING = init_state(*BAD_TEST_SETUP)
assert get_toasted_chip_indexes(BAD_TEST_BUILDING) == [0, 1]
assert is_complete(BAD_TEST_BUILDING) == False




# Both chips should be toast
COMPLETE_TEST_SETUP = [
    ('Hydrogen', 4, 4),
    ('Lithium', 4, 4),
]
COMPLETE_TEST_BUILDING = init_state(*COMPLETE_TEST_SETUP)
assert get_toasted_chip_indexes(COMPLETE_TEST_BUILDING) == []
assert is_complete(COMPLETE_TEST_BUILDING) == True
assert solve(COMPLETE_TEST_BUILDING) == 0






# Test the example moves
# print output(TEST_BUILDING)

def test_move(state, id, direction, *args):
    expected_output = args[-1]
    items = args[:-1]

    new_state = move_state(state, direction, *items)
    # print '\n----- {} -----\n'.format(id)
    # print output(new_state)
    if new_state != expected_output:
        print 'Expected: ', expected_output
        print 'Actual  : ', new_state
    assert new_state == expected_output
    return new_state

TEST_MOVES = [
    (U, (0, M),         (1, [[1, 1], [2, 0]])),
    (U, (0, M), (0, G), (2, [[2, 2], [2, 0]])),
    (D, (0, M),         (1, [[2, 1], [2, 0]])),
    (D, (0, M),         (0, [[2, 0], [2, 0]])),
    (U, (0, M), (1, M), (1, [[2, 1], [2, 1]])),
    (U, (0, M), (1, M), (2, [[2, 2], [2, 2]])),
    (U, (0, M), (1, M), (3, [[2, 3], [2, 3]])),
    (D, (0, M),         (2, [[2, 2], [2, 3]])),
    (U, (0, G), (1, G), (3, [[3, 2], [3, 3]])),
    (D, (1, M),         (2, [[3, 2], [3, 2]])),
    (U, (0, M), (1, M), (3, [[3, 3], [3, 3]])),
]
NEW_TEST_BUILDING = TEST_BUILDING
for id, move_args in enumerate(TEST_MOVES):
    NEW_TEST_BUILDING = test_move(NEW_TEST_BUILDING, id, *move_args)
assert is_complete(NEW_TEST_BUILDING) == True


assert solve(TEST_BUILDING) == 11








# BUILDING = init_state(
#     ('Polonium', 1, 2),
#     ('Thulium', 1, 1),
#     ('Promethium', 1, 2),
#     ('Ruthenium', 1, 1),
#     ('Cobalt', 1, 1),
# )
# BUILDING_INITIAL_OUTPUT = """     0  1  2  3  4
# F4
# F3
# F2    M     M
# F1 E G  GM G  GM GM"""
# print BUILDING.output()
# assert BUILDING.output() == BUILDING_INITIAL_OUTPUT

# BUILDING_MOVES = [
#     (U, (2, M),       ),
#     (U, (1, M), (2, M)),
#     (U, (1, M), (2, M)),
#     (D, (1, M),       ),
#     (D, (1, M),       ),
#     (U, (1, M), (3, M)),
#     (U, (1, M), (3, M)),
#     (D, (1, M),       ),
#     (D, (1, M),       ),
#     (D, (1, M),       ),
#     (U, (1, M), (4, M)),
#     (U, (1, M), (4, M)),
#     (U, (1, M), (4, M)),
#     (D, (1, M),       ),
#     (D, (1, M),       ),
#     (D, (1, M),       ),
#     (U, (1, M), (5, M)),
#     (U, (1, M), (5, M)),
#     (U, (1, M), (5, M)),
# ]
# for id, move in enumerate(BUILDING_MOVES):
#     direction = move[0]
#     items = move[1:]

#     print '\n----- {} -----\n'.format(id)
#     BUILDING.move_state(direction, *items)
#     print BUILDING.output()
