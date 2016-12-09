import re

INPUT = open('07.txt').read()
TLS_PATTERN = r'([a-z])([a-z])\2\1'
BRACKET_START = r'\[[^\]]*'
BRACKET_END = r'[^\[]*\]'
BAD_TLS_PATTERN = BRACKET_START+TLS_PATTERN+BRACKET_END
HYPERNET_PATTERN = BRACKET_START+r'[a-z]*'+BRACKET_END

def supports_tls(ip):
    # print ip
    if re.search(BAD_TLS_PATTERN, ip):
        # print '  BAD'
        return False
    matches = re.findall(TLS_PATTERN, ip)
    for m1, m2 in matches:
        if m1 != m2:
            # print '  GOOD'
            return True
    # print '  OTHER'
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

TEST_INPUT_TLS = """abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn"""
assert count_supports_tls(TEST_INPUT_TLS) == 2
print count_supports_tls(INPUT)
# Got 77 but that's too low :(
# Missed the case where there were multiple hypernets!




def split_ip(ip):
    # supernet = outside brackets
    # hypernet = inside brackets

    # Extract the hypernets
    hypernets = re.findall(HYPERNET_PATTERN, ip)

    # Replace them with a single character we can split on later
    for hypernet in hypernets:
        ip = ip.replace(hypernet, '|')

    # Remove []s
    hypernets = map(lambda hn: hn.replace('[', '').replace(']', ''), hypernets)

    return ip.split('|'), hypernets

assert split_ip('abba[mnop]qrst') == (['abba', 'qrst'], ['mnop'])
assert split_ip('abcd[bddb]xyyx') == (['abcd', 'xyyx'], ['bddb'])
assert split_ip('aaaa[qwer]tyui') == (['aaaa', 'tyui'], ['qwer'])
assert split_ip('ioxxoj[asdfgh]zxcvbn') == (['ioxxoj', 'zxcvbn'], ['asdfgh'])
assert split_ip('zxcvbn[asabbadfgh]ioxxoj') == (['zxcvbn', 'ioxxoj'], ['asabbadfgh'])




def supports_ssl(ip):
    # print
    # print ip
    supernets, hypernets = split_ip(ip)

    for supernet in supernets:
        # print supernet
        for i in xrange(len(supernet) - 2):
            supernet_aba = supernet[i:i+3]
            if supernet_aba[0] == supernet_aba[2] and supernet_aba[0] != supernet_aba[1]:
                # This is a valid aba supernet
                # Check for a valid bab hypernet
                hypernet_bab = supernet_aba[1] + supernet_aba[0] + supernet_aba[1]
                for hypernet in hypernets:
                    if hypernet_bab in hypernet:
                        return True
    return False

assert supports_ssl('aba[bab]xyz') == True
assert supports_ssl('xyx[xyx]xyx') == False
assert supports_ssl('aaa[kek]eke') == True
assert supports_ssl('zazbz[bzb]cdb') == True


def count_supports_ssl(input):
    return len(filter(supports_ssl, input.split('\n')))

TEST_INPUT_SSL = """aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb"""
assert count_supports_ssl(TEST_INPUT_SSL) == 3
print count_supports_ssl(INPUT)
