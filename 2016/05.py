import hashlib

def hash(door_id, index):
    return hashlib.md5(door_id + str(index)).hexdigest()

assert hash('abc', 3231929)[:6] == '000001'
assert hash('abc', 5017308)[:9] == '000008f82'
assert hash('abc', 5278568)[:6] == '00000f'



def get_code(door_id):
    index = 0
    output = ''
    while len(output) < 8:
        hash_output = hash(door_id, index)
        if hash_output[:5] == '00000':
            # print index, '->', hash_output
            output += hash_output[5]
        index += 1
        if index % 1000000 == 0:
            print index, '...'
    # print output
    return output


# assert get_code('abc') == '18f47a30'
# print get_code('ojvtpuvg')




def get_code2(door_id):
    index = 0
    places_filled = 0
    output = [None] * 8
    while places_filled < 8:
        hash_output = hash(door_id, index)
        if hash_output[:5] == '00000':
            print index, '->', hash_output
            position, value = hash_output[5:7]
            if position in '01234567':
                position = int(position)
                if output[position] is None:
                    print '  Filled!'
                    output[position] = value
                    places_filled += 1
        index += 1
        if index % 1000000 == 0:
            print index, '...'
    print output
    return ''.join(output)


assert get_code2('abc') == '05ace8e3'
print get_code2('ojvtpuvg')
