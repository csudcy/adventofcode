INPUT = open('06.txt').read()


def filter_message(lines, reverse=True):
    position_counts = None
    for line in lines.split('\n'):
        if position_counts is None:
            position_counts = [
                {}
                for k in line
            ]
        for index, k in enumerate(line):
            position_counts[index][k] = position_counts[index].get(k, 0) + 1

    output = [
        sorted([
            (v, k)
            for k, v in position_count.iteritems()
        ], reverse=reverse)[0][1]
        for position_count in position_counts
    ]
    print output
    return ''.join(output)


TEST_INPUT = """eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar"""

assert filter_message(TEST_INPUT) == 'easter'
print filter_message(INPUT)

assert filter_message(TEST_INPUT, reverse=False) == 'advent'
print filter_message(INPUT, reverse=False)
