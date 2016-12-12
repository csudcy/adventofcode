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

U = 1
D = -1
G = 'gen'
M = 'chip'

class RTGBuilding(object):
    def __init__(self, *isotopes):
        # isotopes is a list of (name, generator floor, microchip floor)
        self._isotopes = [
            {
                'number': index + 1,
                'name': isotope[0],
                'gen_index': isotope[1] - 1,
                'chip_index': isotope[2] - 1,
            }
            for index, isotope in enumerate(isotopes)
        ]

        # THERE. ARE. FOUR. FLOORS.
        self._floor_count = 4
        self._elevator_floor_index = 0

    def move(self, direction, *items):
        # items is a list of (isotope_number, gen_or_chip)

        # Have to have an item to use the lift
        if len(items) == 0:
            raise Exception('You cannot use the lift without taking an item!')

        # Have to be moving to a valid floor
        new_floor_index = self.get_new_floor_or_none(direction)
        if new_floor_index is None:
            raise Exception(
                'You cannot move {direction} floor from {floor_number}!'.format(
                    direction=direction,
                    floor_number=self._elevator_floor_index+1
                )
            )

        # Check all items are on the same floor as the elevator
        for isotope_number, gen_or_chip in items:
            if not self.can_pickup(isotope_number, gen_or_chip):
                raise Exception(
                    'Isotope {isotope_number} {gen_or_chip} is on floor {floor_number}; you cannot pick it up in the elevator on floor {elevator_floor_number}!'.format(
                        isotope_number=isotope_number,
                        gen_or_chip=gen_or_chip,
                        floor_number=self._isotopes[isotope_number-1][gen_or_chip+'_index']+1,
                        elevator_floor_number=self._elevator_floor_index+1
                    )
                )

        # Move to the new floor
        self._elevator_floor_index = new_floor_index
        for isotope_number, gen_or_chip in items:
            self._isotopes[isotope_number-1][gen_or_chip+'_index'] = new_floor_index

        # Check no chips have died
        toasted_chip_numbers = self.get_toasted_chip_numbers()
        if toasted_chip_numbers:
            raise Exception(
                'You have toasted these chips: {toasted_chip_numbers}'.format(
                    toasted_chip_numbers=toasted_chip_numbers,
                )
            )


        pass

    def get_new_floor_or_none(self, direction):
        new_floor_index = self._elevator_floor_index + direction
        if new_floor_index < 0 or new_floor_index >= 4:
            return None
        return new_floor_index

    def can_pickup(self, isotope_number, gen_or_chip):
        floor_index = self._isotopes[isotope_number-1][gen_or_chip+'_index']
        return floor_index == self._elevator_floor_index

    def get_floors_have_generators(self):
        floors_have_generators = [False] * 4
        for isotope in self._isotopes:
            floors_have_generators[isotope['gen_index']] = True
        return floors_have_generators

    def get_toasted_chip_numbers(self):
        floors_have_generators = self.get_floors_have_generators()
        toasted_chip_numbers = []
        for isotope in self._isotopes:
            # This chip is with it's generator; it is safe
            if isotope['gen_index'] == isotope['chip_index']:
                continue
            # If there are any generators on this chip's floor, the chip is toast
            if floors_have_generators[isotope['chip_index']]:
                toasted_chip_numbers.append(isotope['number'])

        return toasted_chip_numbers

    def is_complete(self):
        for isotope in self._isotopes:
            if isotope['chip_index'] != 3 or isotope['gen_index'] != 3:
                return False
        return True

    def output(self, include_legend=False):
        # Output in a semi-nice way
        output = []

        # Add a legend
        if include_legend:
            output.append('Legend:')
            for isotope in self._isotopes:
                output.append('{0}={1}'.format(isotope['number'], isotope['name']))
            output.append('')

        # Add the isotope header
        header = '     '
        for isotope in self._isotopes:
            header += str(isotope['number']) + '  '
        output.append(header)

        # Add the floors
        floors_output = []
        for floor_index in xrange(self._floor_count):
            floor_output = [
                # Add the floor identifier
                'F' + str(floor_index+1),
                # Add if the elevator is here
                'E' if self._elevator_floor_index == floor_index else ' '
            ]
            for isotope in self._isotopes:
                floor_output.append(
                    ('G' if isotope['gen_index'] == floor_index else ' ') +
                    ('M' if isotope['chip_index'] == floor_index else ' ')
                )
            floors_output.append(' '.join(floor_output))

        output += reversed(floors_output)

        return '\n'.join([
            line.rstrip()
            for line in output
        ])

    def output_compact(self):
        # Output the current state as:
        # (
        #   Elevator floor number,
        #   [(isotope number, generator floor, microchip floor), ...]
        # )

        return (
            self._elevator_floor_index+1,
            [
                (
                    isotope['number'],
                    isotope['gen_index'] + 1,
                    isotope['chip_index'] + 1,
                )
                for isotope in self._isotopes
            ]
        )

EXPECTED_TEST_OUTPUT = """Legend:
1=Hydrogen
2=Lithium

     1  2
F4
F3      G
F2   G
F1 E  M  M"""

TEST_SETUP = [
    ('Hydrogen', 2, 1),
    ('Lithium', 3, 1),
]
TEST_BUILDING = RTGBuilding(*TEST_SETUP)
assert TEST_BUILDING.output_compact() == (1, [(1, 2, 1), (2, 3, 1)])
assert TEST_BUILDING.output(include_legend=True) == EXPECTED_TEST_OUTPUT
assert TEST_BUILDING.get_new_floor_or_none(0) == 0
assert TEST_BUILDING.get_new_floor_or_none(1) == 1
assert TEST_BUILDING.get_new_floor_or_none(3) == 3
assert TEST_BUILDING.get_new_floor_or_none(-1) == None
assert TEST_BUILDING.get_new_floor_or_none(4) == None
assert TEST_BUILDING.can_pickup(1, M) == True
assert TEST_BUILDING.can_pickup(1, G) == False
assert TEST_BUILDING.can_pickup(2, M) == True
assert TEST_BUILDING.can_pickup(2, G) == False
assert TEST_BUILDING.get_floors_have_generators() == [False, True, True, False]
assert TEST_BUILDING.get_toasted_chip_numbers() == []
assert TEST_BUILDING.is_complete() == False

# Both chips should be toast
BAD_TEST_SETUP = [
    ('Hydrogen', 2, 1),
    ('Lithium', 1, 2),
]
BAD_TEST_BUILDING = RTGBuilding(*BAD_TEST_SETUP)
assert BAD_TEST_BUILDING.get_toasted_chip_numbers() == [1, 2]

# Both chips should be toast
COMPLETE_TEST_SETUP = [
    ('Hydrogen', 4, 4),
    ('Lithium', 4, 4),
]
COMPLETE_TEST_BUILDING = RTGBuilding(*COMPLETE_TEST_SETUP)
assert COMPLETE_TEST_BUILDING.get_toasted_chip_numbers() == []
assert COMPLETE_TEST_BUILDING.is_complete() == True

# Test the example moves
# print TEST_BUILDING.output(include_legend=True)

def test_move(id, direction, *args):
    expected_output = args[-1]
    items = args[:-1]

    TEST_BUILDING.move(direction, *items)
    # print '\n----- {} -----\n'.format(id)
    # print TEST_BUILDING.output()
    actual_output = TEST_BUILDING.output_compact()
    if actual_output != expected_output:
        print 'Expected: ', expected_output
        print 'Actual  : ', actual_output
    assert actual_output == expected_output

TEST_MOVES = [
    (U, (1, M),         (2, [(1, 2, 2), (2, 3, 1)])),
    (U, (1, M), (1, G), (3, [(1, 3, 3), (2, 3, 1)])),
    (D, (1, M),         (2, [(1, 3, 2), (2, 3, 1)])),
    (D, (1, M),         (1, [(1, 3, 1), (2, 3, 1)])),
    (U, (1, M), (2, M), (2, [(1, 3, 2), (2, 3, 2)])),
    (U, (1, M), (2, M), (3, [(1, 3, 3), (2, 3, 3)])),
    (U, (1, M), (2, M), (4, [(1, 3, 4), (2, 3, 4)])),
    (D, (1, M),         (3, [(1, 3, 3), (2, 3, 4)])),
    (U, (1, G), (2, G), (4, [(1, 4, 3), (2, 4, 4)])),
    (D, (2, M),         (3, [(1, 4, 3), (2, 4, 3)])),
    (U, (1, M), (2, M), (4, [(1, 4, 4), (2, 4, 4)])),
]

for id, move in enumerate(TEST_MOVES):
    test_move(id, *move)

assert TEST_BUILDING.is_complete() == True





BUILDING = RTGBuilding(
    ('Polonium', 1, 2),
    ('Thulium', 1, 1),
    ('Promethium', 1, 2),
    ('Ruthenium', 1, 1),
    ('Cobalt', 1, 1),
)
BUILDING_INITIAL_OUTPUT = """Legend:
1=Polonium
2=Thulium
3=Promethium
4=Ruthenium
5=Cobalt

     1  2  3  4  5
F4
F3
F2    M     M
F1 E G  GM G  GM GM"""
print BUILDING.output(include_legend=True)
assert BUILDING.output(include_legend=True) == BUILDING_INITIAL_OUTPUT

BUILDING_MOVES = [
    (U, (2, M),       ),
    (U, (1, M), (2, M)),
    (U, (1, M), (2, M)),
    (D, (1, M),       ),
    (D, (1, M),       ),
    (U, (1, M), (3, M)),
    (U, (1, M), (3, M)),
    (D, (1, M),       ),
    (D, (1, M),       ),
    (D, (1, M),       ),
    (U, (1, M), (4, M)),
    (U, (1, M), (4, M)),
    (U, (1, M), (4, M)),
    (D, (1, M),       ),
    (D, (1, M),       ),
    (D, (1, M),       ),
    (U, (1, M), (5, M)),
    (U, (1, M), (5, M)),
    (U, (1, M), (5, M)),
]
for id, move in enumerate(BUILDING_MOVES):
    direction = move[0]
    items = move[1:]

    print '\n----- {} -----\n'.format(id)
    BUILDING.move(direction, *items)
    print BUILDING.output()
