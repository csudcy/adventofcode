import re

INPUT = open('07.txt').read()
PATTERN = r'([a-z])([a-z])\2\1'
BAD_PATTERN = r'\[[^\]]*'+PATTERN+r'[^\[]*\]'

def supports_tls(ip):
    print ip
    if re.search(BAD_PATTERN, ip):
        print '  BAD'
        return False
    matches = re.findall(PATTERN, ip)
    for m1, m2 in matches:
        if m1 != m2:
            print '  GOOD'
            return True
    print '  OTHER'
    return False

assert supports_tls('abba[mnop]qrst') == True
assert supports_tls('abcd[bddb]xyyx') == False
assert supports_tls('aaaa[qwer]tyui') == False
assert supports_tls('ioxxoj[asdfgh]zxcvbn') == True
assert supports_tls('zxcvbn[asabbadfgh]ioxxoj') == False
# Guess this is acceptable?
assert supports_tls('zxcaaaavbn[asdfgh]ioxxoj') == True
assert supports_tls('zxcaaabn[asdfgh]ioxxoj') == True
assert supports_tls('abcd[efgh]ijkl[mnop]qrst') == False
assert supports_tls('abba[efgh]ijkl[mnop]qrst') == True
assert supports_tls('abcd[efgh]ijji[mnop]qrst') == True
assert supports_tls('abcd[efgh]ijkl[mnop]qrrq') == True
assert supports_tls('abba[effe]ijkl[mnop]qrst') == False
assert supports_tls('abcd[efgh]ijji[mnnm]qrst') == False
assert supports_tls('abba[effe]ijji[mnnm]qrrq') == False


def count_supports_tls(input):
    return len(filter(supports_tls, input.split('\n')))

TEST_INPUT = """abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn"""
assert count_supports_tls(TEST_INPUT) == 2
print count_supports_tls(INPUT)
# Got 77 but that's too low :(
