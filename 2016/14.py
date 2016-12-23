import md5
import re

HASH_MEMO = {}

def get_hash(stretch_count, salt, index):
    key = (stretch_count, salt, index)
    if key not in HASH_MEMO:
        hash = md5.new(salt + str(index)).hexdigest()
        for i in xrange(stretch_count):
            hash = md5.new(hash).hexdigest()
        HASH_MEMO[key] = hash
    return HASH_MEMO[key]


TRIPLE_RE = r'(.)\1{2,}'

def get_triple(stretch_count, salt, index):
    hash = get_hash(stretch_count, salt, index)
    matches = re.search(TRIPLE_RE, hash)
    # import pdb
    # pdb.set_trace()
    if matches:
        return matches.group(1)
    pass


def has_quintuple(stretch_count, salt, index, char):
    hash = get_hash(stretch_count, salt, index)
    return char*5 in hash


def is_key(stretch_count, salt, index):
    char = get_triple(stretch_count, salt, index)
    if char is None:
        return False

    # Check the next 1000 hashes
    for check_index in xrange(index+1, index+1001):
        if has_quintuple(stretch_count, salt, check_index, char):
            print index, check_index, char, get_hash(stretch_count, salt, index), get_hash(stretch_count, salt, check_index)
            return True
    
    return False


def check_keys(stretch_count, salt, key_count):
    found_keys = []

    for index in xrange(1000000):
        if is_key(stretch_count, salt, index):
            found_keys.append(index)
            if len(found_keys) == key_count:
                print found_keys
                return index


assert 'cc38887a5' in get_hash(0, 'abc', 18)
assert get_triple(0, 'abc', 18) == '8'
assert has_quintuple(0, 'abc', 18, '8') == False
assert is_key(0, 'abc', 18) == False

assert get_triple(0, 'abc', 39) == 'e'
assert has_quintuple(0, 'abc', 816, 'e') == True
assert is_key(0, 'abc', 39) == True

assert get_triple(0, 'abc', 92) == '9'
assert has_quintuple(0, 'abc', 200, '9') == True
assert is_key(0, 'abc', 92) == True

assert is_key(0, 'abc', 22728) == True

# assert check_keys(0, 'abc', 64) == 22728

# print check_keys(0, 'yjdafjpo', 64)


assert get_triple(2016, 'abc', 5) == '2'
assert is_key(2016, 'abc', 5) == False

assert get_triple(2016, 'abc', 10) == 'e'
assert has_quintuple(2016, 'abc', 89, 'e') == True
assert is_key(2016, 'abc', 10) == True

assert get_triple(2016, 'abc', 22551) == 'f'
assert has_quintuple(2016, 'abc', 22859, 'f') == True
assert is_key(2016, 'abc', 22551) == True

assert check_keys(2016, 'abc', 64) == 22551

print check_keys(2016, 'yjdafjpo', 64)

