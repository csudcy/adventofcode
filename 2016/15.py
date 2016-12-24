INPUT = open('15.txt').read()
TEST_INPUT = """Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1."""


def setup_discs(input):
    discs = []
    for line in input.split('\n'):
        bits = line.split(' ')
        positions = int(bits[3])
        start_position = int(bits[-1][:-1])
        discs.append((positions, start_position))

    return discs

TEST_DISCS = setup_discs(TEST_INPUT)
assert TEST_DISCS == [(5, 4), (2, 1)]


def can_pass(discs, start_time, disc_index):
    positions, start_position = discs[disc_index]
    return ((start_position + start_time + disc_index + 1) % positions) == 0

assert can_pass(TEST_DISCS, 0, 0) == True
assert can_pass(TEST_DISCS, 0, 1) == False

assert can_pass(TEST_DISCS, 5, 0) == True
assert can_pass(TEST_DISCS, 5, 1) == True


def can_all_pass(discs, start_time):
    return all(
        map(
            lambda disc_index: can_pass(discs, start_time, disc_index),
            xrange(len(discs))
        )
    )

assert can_all_pass(TEST_DISCS, 0) == False
assert can_all_pass(TEST_DISCS, 5) == True


def get_first_pass(discs):
    for i in xrange(10000000):
        if can_all_pass(discs, i):
            return i
        if i % 10000 == 0:
            print i

assert get_first_pass(TEST_DISCS) == 5

DISCS = setup_discs(INPUT)
# print get_first_pass(DISCS)


DISCS_2 = DISCS + [(11, 0)]
print get_first_pass(DISCS_2)



