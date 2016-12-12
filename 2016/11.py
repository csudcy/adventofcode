"""
Initial setup:

1=polonium generator
2=thulium generator
3=promethium generator
4=ruthenium generator
5=cobalt generator

     1  2  3  4  5
F4
F3
F2    M     M
F1 E G  GM G  GM GM

Make a simulator to check correctness & give it moves?

MOVES = [
    (U, (2,M), (,)),
    (D, (2,M), (3,M)),
    (U, (1,G), (,)),
]
"""

U = 1
D = -1
G = 0
M = 1

class RTGBuilding(object):
    def __init__(self, *isotopes):
        # isotopes is a list of (name, generator floor, microchip floor)
        self._isotope_names = []
        # THERE. ARE. FOUR. FLOORS.
        self._floors = [
            {},
            {},
            {},
            {},
        ]
        for name, gen_floor, chip_floor in isotopes:
            # Convert to 0-based floor numbering
            gen_floor -= 1
            chip_floor -= 1

            # Add this isotope to the list & to the floors
            self._isotope_names.append(name)
            for floor_number, floor in enumerate(self._floors):
                floor[name] = {
                    'has_gen': floor_number == gen_floor,
                    'has_chip': floor_number == chip_floor,
                }

        self._elevator_floor = 0

    def move(self, direction, *items):
        # items is a list of (isotope_index, gen_or_chip)

        # Have to have an item to use the lift
        if len(items) == 0:
            raise Exception('You cannot use the lift without taking an item!')

        # Have to be moving to a valid floor
        new_floor = self._elevator_floor + direction
        if new_floor < 0 or new_floor >= 4:
            raise Exception('You cannot move to floor ' + new_floor)

        # Check the change isn't going to kill any chips
        
        pass

    def output(self, include_legend=False):
        # Output in a semi-nice way
        output = []

        # Add a legend
        if include_legend:
            output.append('Legend:')
            for index, isotope in enumerate(self._isotope_names):
                output.append('{0}={1}'.format(index+1, isotope))
            output.append('')

        # Add the isotope header
        header = '     '
        for index in xrange(len(self._isotope_names)):
            header += str(index+1) + '  '
        output.append(header)

        # Add the floors
        floors_output = []
        for floor_number, floor in enumerate(self._floors):
            floor_output = [
                # Add the floor identifier
                'F' + str(floor_number+1),
                # Add if the elevator is here
                'E' if self._elevator_floor == floor_number else ' '
            ]
            for index, isotope in enumerate(self._isotope_names):
                floor_output.append(
                    ('G' if floor[isotope]['has_gen'] else ' ') +
                    ('M' if floor[isotope]['has_chip'] else ' ')
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
        #   [(name, generator floor, microchip floor), ...]
        # )

        # Work out where all the generators and chips currently are
        current_floors = {}
        for isotope in self._isotope_names:
            current_floors[isotope] = {
                'gen': None,
                'chip': None
            }
        for index, floor in enumerate(self._floors):
            for isotope in self._isotope_names:
                if floor[isotope]['has_gen']:
                    current_floors[isotope]['gen'] = index + 1
                if floor[isotope]['has_chip']:
                    current_floors[isotope]['chip'] = index + 1

        # Return the info in a compact format
        return (
            self._elevator_floor+1,
            [
                (index+1, current_floors[isotope]['gen'], current_floors[isotope]['chip'])
                for index, isotope in enumerate(self._isotope_names)
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
TEST_BUILDING.move(U, (1, G))
print TEST_BUILDING.output(include_legend=True)
assert TEST_BUILDING.output_compact() == (2, [(1, 2, 2), (2, 3, 1)])








