INPUT = open('08.txt').read()


def init_board(w, h):
    return [
        [
            False
            for x in xrange(w)
        ]
        for y in xrange(h)
    ]

def apply_command_rect(board, options):
    # print 'apply_command_rect'
    w, h = map(int, options.split('x'))
    # print w, h
    for x in xrange(w):
        for y in xrange(h):
            board[y][x] = True

    return board

def apply_command_rrow(board, options):
    # print 'apply_command_rrow'

    # Get the parameters
    row_index, rotate_by = map(int, options.split(' by '))
    # print row_index, rotate_by

    # Get what the current row looks like
    current_row = board[row_index]

    # Work out what the new row will look like
    w = len(current_row)
    new_row = [
        current_row[(x-rotate_by+w) % w]
        for x in xrange(w)
    ]

    # Stick new values back in the board
    board[row_index] = new_row

    return board

def apply_command_rcol(board, options):
    # print 'apply_command_rcol'

    # Get the parameters
    col_index, rotate_by = map(int, options.split(' by '))
    # print col_index, rotate_by

    # Get what the current column looks like
    current_col = [
        row[col_index]
        for row in board
    ]

    # Work out what the new column will look like
    h = len(current_col)
    new_col = [
        current_col[(y-rotate_by+h) % h]
        for y in xrange(h)
    ]

    # Stick new values back in the board
    for y in xrange(h):
        board[y][col_index] = new_col[y]

    return board

def apply_command(board, command):
    if command[:4] == 'rect':
        return apply_command_rect(board, command[5:])
    if command[:13] == 'rotate row y=':
        return apply_command_rrow(board, command[13:])
    if command[:16] == 'rotate column x=':
        return apply_command_rcol(board, command[16:])
    raise Exception('Unknown command: ' + command)

def output_board(board):
    return '\n'.join(
        map(
            lambda row: ''.join(
                map(
                    lambda cell: '#' if cell else '.',
                    row
                )
            ),
            board
        )
    )

TEST_INIT = (
    '.......\n'
    '.......\n'
    '.......'
)

TEST_STEPS = [
    (
        'rect 3x2',
        '###....\n'
        '###....\n'
        '.......'
    ), (
        'rotate column x=1 by 1',
        '#.#....\n'
        '###....\n'
        '.#.....'
    ), (
        'rotate row y=0 by 4',
        '....#.#\n'
        '###....\n'
        '.#.....'
    ), (
        'rotate column x=1 by 1',
        '.#..#.#\n'
        '#.#....\n'
        '.#.....'
    )
]

TEST_BOARD = init_board(7, 3)
assert output_board(TEST_BOARD) == TEST_INIT
for command, expected_board in TEST_STEPS:
    print
    print command
    TEST_BOARD = apply_command(TEST_BOARD, command)
    print output_board(TEST_BOARD)
    assert output_board(TEST_BOARD) == expected_board

def apply_commands(board, input):
    for command in input.split('\n'):
        board = apply_command(board, command)
    return board

def count_lit(board):
    count = 0
    for row in board:
        for cell in row:
            if cell:
                count += 1
    return count

INITIAL_BOARD = init_board(50, 6)
APPLIED_BOARD = apply_commands(INITIAL_BOARD, INPUT)
print output_board(APPLIED_BOARD)
print count_lit(APPLIED_BOARD)
