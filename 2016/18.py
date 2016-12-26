INPUT = '^..^^.^^^..^^.^...^^^^^....^.^..^^^.^.^.^^...^.^.^.^.^^.....^.^^.^.^.^.^.^.^^..^^^^^...^.....^....^.'

IS_TRAP = {
    # (left, centre, right) -> new_row
    (False, False, False): False,
    (False, False,  True):  True,
    (False,  True, False): False,
    (False,  True,  True):  True,
    ( True, False, False):  True,
    ( True, False,  True): False,
    ( True,  True, False):  True,
    ( True,  True,  True): False,
}


def parse_row(row):
    return [False] + [
        c == '^'
        for c in row
    ] + [False]

assert parse_row('...') == [False, False, False, False, False]
assert parse_row('^^^') == [False, True, True, True, False]


def output_row(parsed_row):
    return ''.join([
        '^' if c else '.'
        for c in parsed_row[1:-1]
    ])

assert output_row([False, False, False, False, False]) == '...'
assert output_row([False, True, True, True, False]) == '^^^'


def next_row(parsed_row):
    return [False] + [
        IS_TRAP[(parsed_row[i], parsed_row[i+1], parsed_row[i+2])]
        for i in xrange(len(parsed_row) - 2)
    ] + [False]

assert output_row(next_row(parse_row('..^^.'))) == '.^^^^'
assert output_row(next_row(parse_row('.^^.^.^^^^'))) == '^^^...^..^'


def get_map(first_row, row_count):
    row = parse_row(first_row)
    output_rows = [output_row(row)]
    while len(output_rows) < row_count:
        row = next_row(row)
        output_rows.append(output_row(row))
    return '\n'.join(output_rows)

TEST1_INPUT = '..^^.'
TEST1_MAP = """..^^.
.^^^^
^^..^"""

TEST2_INPUT = ".^^.^.^^^^"
TEST2_MAP = """.^^.^.^^^^
^^^...^..^
^.^^.^.^^.
..^^...^^^
.^^^^.^^.^
^^..^.^^..
^^^^..^^^.
^..^^^^.^^
.^^^..^.^^
^^.^^^..^^"""


assert get_map(TEST1_INPUT, 3) == TEST1_MAP
assert get_map(TEST2_INPUT, 10) == TEST2_MAP


INPUT_MAP = get_map(INPUT, 40)
print INPUT_MAP
print INPUT_MAP.count('.')


print get_map(INPUT, 400000).count('.')
