
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



def generate_map(w, h, number):
    return '\n'.join([
        ''.join([
            '.' if is_open(x, y, number) else '#'
            for x in xrange(w)
        ])
        for y in xrange(h)
    ])


assert generate_map(10, 7, TEST_NUMBER) == TEST_MAP_OUTPUT



def find_route(x, y, tx, ty, number):
    pass

print find_route(1, 1, 7, 4, 10)
assert find_route(1, 1, 7, 4, 10) == 11
