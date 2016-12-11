INPUT = open('09.txt').read().strip()

import time


def expand(input):
    index = 0
    output = ''
    while True:
        # Find the next open bracket
        try:
            start_index = input.index('(', index)
        except ValueError:
            # No more commands
            # Add on anything remaining from the previous command & exit
            output += input[index:]
            break

        # Add on everything between end of the previous command & the start of this one
        output += input[index:start_index]

        # Extract the command
        end_index = input.index(')', start_index)
        command = input[start_index+1:end_index]
        length, count = map(int, command.split('x'))
        # print length, count

        # Add the repeated string
        repeat = input[end_index+1:end_index+1+length]
        # print repeat
        output += repeat * count

        # Move on
        index = end_index + 1 + length

        # break

    # print output
    return output

assert expand('ADVENT') == 'ADVENT'
assert expand('A(1x5)BC') == 'ABBBBBC'
assert expand('(3x3)XYZ') == 'XYZXYZXYZ'
assert expand('A(2x2)BCD(2x2)EFG') == 'ABCBCDEFEFG'
assert expand('(6x1)(1x3)A') == '(1x3)A'
assert expand('X(8x2)(3x3)ABCY') == 'X(3x3)ABC(3x3)ABCY'

print len(expand(INPUT))
# Got 3608; that's too low :(
# Read the wrong input file - d'oh!


def expandv2_length(input):
    total_length = 0
    iters = 0
    remaining_input = input
    start_time = time.time()
    next_time = time.time()
    while True:
        # Find the next open bracket
        try:
            start_index = remaining_input.index('(')
        except ValueError:
            # No more commands
            # Add on anything remaining from the previous command & exit
            total_length += len(remaining_input)
            break

        # Count everything before the start of this command
        total_length += start_index

        # Extract the command
        end_index = remaining_input.index(')', start_index)
        command = remaining_input[start_index+1:end_index]
        length, count = map(int, command.split('x'))
        # print length, count

        # Get the repeated string
        repeat = remaining_input[end_index+1:end_index+1+length]
        # print repeat

        # Remove the this command, everything before it & everything used by it
        # Prepend the result of this command
        remaining_input = repeat * count + remaining_input[end_index+1+length:]
        iters += 1

        if time.time() > next_time:
            diff_time = time.time() - start_time
            print '{diff_time:.02f}s : {total_length} done, {remaining_input} to go'.format(
                diff_time=diff_time,
                total_length=total_length,
                remaining_input=len(remaining_input),
            )
            next_time = time.time() + 1

        # break

    print total_length
    return total_length


assert expandv2_length('(3x3)XYZ') == len('XYZXYZXYZ')
assert expandv2_length('X(8x2)(3x3)ABCY') == len('XABCABCABCABCABCABCY')
assert expandv2_length('(27x12)(20x12)(13x14)(7x10)(1x12)A') == 241920
assert expandv2_length('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN') == 445

# print expandv2_length(INPUT)
# This took about half an hour and came to 10910125505 (or just over 10GB!)
