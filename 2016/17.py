INPUT = 'udskfozm'

import md5

# Make some constants
U, D, L, R = 'UDLR'
POSITIONS = [U, D, L, R]
OPEN_DOORS = 'bcdef'

def get_open_doors(key, path):
    hash = md5.new(key + path).hexdigest()
    return [
        d
        for i, d in enumerate(POSITIONS)
        if hash[i] in OPEN_DOORS
    ]

assert get_open_doors('hijkl', '') == [U, D, L]
assert get_open_doors('hijkl', 'D') == [U, L, R]
assert get_open_doors('hijkl', 'DR') == []
assert get_open_doors('hijkl', 'DU') == [R]
assert get_open_doors('hijkl', 'DUR') == []



DIRECTIONS = {
    U: (0, -1),
    D: (0, +1),
    L: (-1, 0),
    R: (+1, 0),
}

def get_possible_directions(x, y, key, path):
    # Return a list of (new_x, new_y, new_path)
    open_directions = get_open_doors(key, path)
    possible_directions = []
    for open_direction in open_directions:
        new_x = x + DIRECTIONS[open_direction][0]
        if new_x < 0 or new_x >= 4:
            continue

        new_y = y + DIRECTIONS[open_direction][1]
        if new_y < 0 or new_y >= 4:
            continue

        possible_directions.append((new_x, new_y, path + open_direction))

    return possible_directions

assert get_possible_directions(0, 0, 'hijkl', '') == [(0, 1, 'D')]
assert get_possible_directions(0, 1, 'hijkl', 'D') == [(0, 0, 'DU'), (1, 1, 'DR')]


def get_shortest_path(key, start_x=0, start_y=0, target_x=3, target_y=3):
    to_visit = [
        # (x, y, path)
        (start_x, start_y, '')
    ]

    while to_visit:
        # Get the next location/path to try
        x, y, path = to_visit.pop(0)

        # Check all of the possibl directions
        possible_directions = get_possible_directions(x, y, key, path)
        for new_x, new_y, new_path in possible_directions:
            # Have we reached the target yet?
            if new_x == target_x and new_y == target_y:
                # print new_path
                return new_path

            to_visit.append((new_x, new_y, new_path))

        # print '\n'*3
        # print to_visit


assert get_shortest_path('ihgpwlah') == 'DDRRRD'
assert get_shortest_path('kglvqrro') == 'DDUDRLRRUDRD'
assert get_shortest_path('ulqzkmiv') == 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'

print get_shortest_path(INPUT)
