INPUT = 1352

TEST_NUMBER = 10
TEST_MAP_OUTPUT = """.#.####.##
..#..#...#
#....##...
###.#.###.
.##..#..#.
..##....#.
#...##.###"""


def is_open(x, y, number):
    num = x*x + 3*x + 2*x*y + y + y*y + number
    return bin(num).count('1') % 2 == 0

assert is_open(0, 0, TEST_NUMBER) == True
assert is_open(1, 0, TEST_NUMBER) == False



def generate_map(number, w=None, h=None, route=[]):
    def get_char(x, y):
        if not is_open(x, y, number):
            return '#'
        if (x, y) in route:
            return 'O'
        return '.'

    if route:
        if w is None:
            w = max(map(lambda p: p[0], route)) + 1
        if h is None:
            h = max(map(lambda p: p[1], route)) + 1

    return '\n'.join([
        ''.join([
            get_char(x, y)
            for x in xrange(w)
        ])
        for y in xrange(h)
    ])


assert generate_map(TEST_NUMBER, 10, 7) == TEST_MAP_OUTPUT


DIRECTIONS = [
    (-1, 0),
    (0, -1),
    (+1, 0),
    (0, +1),
]

def find_route(start_x, start_y, target_x, target_y, number):
    visited = [
        (start_x, start_y)
    ]
    to_visit = [
        # x, y, route
        (start_x, start_y, [(start_x, start_y)])
    ]
    while to_visit:
        x, y, route = to_visit.pop(0)

        # Try each direction from here
        for diff_x, diff_y in DIRECTIONS:
            # Work out the next space to visit
            next_x = x + diff_x
            next_y = y + diff_y

            # Check it is on the map
            if next_x < 0 or next_y < 0:
                continue

            # Check we haven't visited it before
            if (next_x, next_y) in visited:
                continue

            # Check it is open
            if not is_open(next_x, next_y, number):
                continue

            # Check if we are at the target
            next_route = route + [(next_x, next_y)]
            if next_x == target_x and next_y == target_y:
                print generate_map(number, route=next_route)
                # print next_route
                return len(next_route) - 1

            # Add it to the list to visit
            to_visit.append(
                (next_x, next_y, next_route)
            )

            # Don't visit it again
            visited.append(
                (next_x, next_y)
            )

    print 'No route found'

assert find_route(1, 1, 7, 4, 10) == 11

print find_route(1, 1, 31, 39, INPUT)
# Got 89; too low :(
# Start Y was wrong




def find_points(start_x, start_y, max_steps, number):
    visited = [
        (start_x, start_y)
    ]
    to_visit = [
        # x, y, route
        (start_x, start_y, [(start_x, start_y)])
    ]
    while to_visit:
        x, y, route = to_visit.pop(0)

        # Try each direction from here
        for diff_x, diff_y in DIRECTIONS:
            # Work out the next space to visit
            next_x = x + diff_x
            next_y = y + diff_y

            # Check it is on the map
            if next_x < 0 or next_y < 0:
                continue

            # Check we haven't visited it before
            if (next_x, next_y) in visited:
                continue

            # Check it is open
            if not is_open(next_x, next_y, number):
                continue

            # Check if we have steps remaining
            next_route = route + [(next_x, next_y)]
            if len(route) > max_steps:
                continue

            # Add it to the list to visit
            to_visit.append(
                (next_x, next_y, next_route)
            )

            # Don't visit it again
            visited.append(
                (next_x, next_y)
            )

    return len(visited)

print find_points(1, 1, 50, INPUT)
# Got 132; too low
# Max_step checking was off-by-one
