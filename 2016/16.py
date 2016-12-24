
def extend(data):
    return data + '0' + ''.join(
        (
            '0' if d == '1' else '1'
            for d in data[::-1]
        )
    )

assert extend('1') == '100'
assert extend('0') == '001'
assert extend('11111') == '11111000000'
assert extend('111100001010') == '1111000010100101011110000'


def extend_until(data, length):
    while len(data) < length:
        data = extend(data)
    return data[:length]

assert extend_until('10000', 20) == '10000011110010000111'

CHECKSUM = {
    '00': '1',
    '11': '1',
    '10': '0',
    '01': '0',
}

def checksum(data):
    cs = ''.join(
        CHECKSUM[data[index:index+2]]
        for index in xrange(0, len(data), 2)
    )

    # If the checksum length is even, do it again
    if len(cs) % 2 == 0:
        return checksum(cs)

    # Otherwise, we are done
    return cs

assert checksum('110010110100') == '100'


def extend_and_checksum(data, length):
    extended_data = extend_until(data, length)
    return checksum(extended_data)

assert extend_and_checksum('10000', 20) == '01100'

INPUT = '00101000101111010'
print extend_and_checksum(INPUT, 272)
print extend_and_checksum(INPUT, 35651584)
