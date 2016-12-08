import re

INPUT = open('04.txt').read()

def parse_room_code(room_code):
    assert re.match(r'([a-z]+-)+\d{3}\[[a-z]{5}\]', room_code)
    room_name = room_code[:-11]
    sector_id = int(room_code[-10:-7])
    check_sum = room_code[-6:-1]
    return room_name, sector_id, check_sum

def parse_input(input):
    return [
        parse_room_code(room_code)
        for room_code in input.split('\n')
    ]

def calculate_checksum(room_name):
    counts = [
        (room_name.count(unique_letter), -ord(unique_letter), unique_letter)
        for unique_letter in set(room_name.replace('-', ''))
    ]
    counts.sort(reverse=True)
    return ''.join(map(lambda x: x[2], counts[:5]))

def validate_room(room):
    test_check_sum = calculate_checksum(room[0])
    return test_check_sum == room[2]

def sum_valid_sectors(input):
    return sum(
        map(
            lambda room: room[1],
            filter(
                validate_room,
                parse_input(input)
            )
        )
    )


assert validate_room(parse_room_code('aaaaa-bbb-z-y-x-123[abxyz]')) == True
assert validate_room(parse_room_code('a-b-c-d-e-f-g-h-987[abcde]')) == True
assert validate_room(parse_room_code('not-a-real-room-404[oarel]')) == True
assert validate_room(parse_room_code('totally-real-room-200[decoy]')) == False
assert validate_room(parse_room_code('aaaaa-bbb-z-y-x-123[abxzy]')) == False

TEST_INPUT = """aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]
aaaaa-bbb-z-y-x-123[abxzy]"""
assert sum_valid_sectors(TEST_INPUT) == 1514

print sum_valid_sectors(INPUT)


def decrypt_room_name(room):
    ord_a = ord('a')
    output = ''
    for k in room[0]:
        if k == '-':
            output += ' '
        else:
            output += chr((ord(k) - ord_a + room[1]) % 26 + ord_a)
    return room[0], room[1], room[2], output

def decrypt_valid_room_names(input):
    return map(
        decrypt_room_name,
        filter(
            validate_room,
            parse_input(input)
        )
    )

def find_north_pole(input):
    return filter(
        lambda x: 'north' in x[3],
        decrypt_valid_room_names(input)
    )

assert decrypt_room_name(parse_room_code('qzmt-zixmtkozy-ivhz-343[abcde]'))[3] == 'very encrypted name'
print find_north_pole(INPUT)
