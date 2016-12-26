NEXT_ELF_INDEX, PRESENT_COUNT = range(2)

def generate_elves(count):
    # Return a list of (next_elf_index, present_count)
    return [
        ((i+1) % count, 1)
        for i in xrange(count)
    ]

assert generate_elves(1) == [(0, 1)]
assert generate_elves(3) == [(1, 1), (2, 1), (0, 1)]


def move_presents_once(elves):
    elf_count = len(elves)
    elf_index = 0
    while True:
        # Skip elves with no presents
        while elves[elf_index][PRESENT_COUNT] == 0:
            elf_index = (elf_index + 1) % elf_count

        next_elf_index, present_count = elves[elf_index]

        # Move to the next next_elf_index with presents
        while elves[next_elf_index][PRESENT_COUNT] == 0:
            next_elf_index = (next_elf_index + 1) % elf_count

        # If I am the only elf with presents left, we're done
        total_present_count = present_count + elves[next_elf_index][PRESENT_COUNT]
        if total_present_count == elf_count:
            return elf_index + 1

        # Update elf status
        elves[elf_index] = ((next_elf_index+1) % elf_count, total_present_count)
        elves[next_elf_index] = (-1, 0)

        # Move to the next elf which might have presents
        elf_index = (next_elf_index + 1) % elf_count

assert move_presents_once(generate_elves(5)) == 3

print move_presents_once(generate_elves(3017957))
