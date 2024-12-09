from AoCUtils.utils import *


def part_one():
    sparse_input, _, _ = expand(parse_input("input1.txt")[0])

    left, right = 0, len(sparse_input) - 1
    while left < right:
        while sparse_input[left] != ".":
            left += 1
        while sparse_input[right] == ".":
            right -= 1

        if left >= right:
            break

        sparse_input[left], sparse_input[right] = (
            sparse_input[right],
            sparse_input[left],
        )

    checksum = 0
    for idx, c in enumerate(sparse_input):
        if c == ".":
            break
        checksum += idx * int(c)
    return checksum


def part_two():
    sparse_input, file_blocks, free_blocks = expand(parse_input("input2.txt")[0])

    for id in sorted(file_blocks.keys(), reverse=True):
        size, index = file_blocks[id]
        for key in sorted(free_blocks.keys()):
            if free_blocks[key] >= size and key < index:
                tmp = sparse_input[key : key + size]
                sparse_input[key : key + size] = sparse_input[index : index + size]
                sparse_input[index : index + size] = tmp

                if free_blocks[key] != size:
                    free_blocks[key + size] = free_blocks[key] - size
                del free_blocks[key]
                break

    checksum = 0
    for idx, c in enumerate(sparse_input):
        if c == ".":
            continue
        checksum += idx * int(c)
    return checksum


def expand(dense):
    file_blocks = {}
    free_blocks = {}
    sparse_input = []
    size = 0
    id = 0

    for index, c in enumerate(dense):
        # File Block
        if index % 2 == 0:
            sparse_input.extend([str(id) for _ in range(int(c))])
            file_blocks[id] = (int(c), size)
            id += 1
        # Free Space
        else:
            sparse_input.extend(["." for _ in range(int(c))])
            free_blocks[size] = int(c)
        size += int(c)

    return sparse_input, file_blocks, free_blocks


run_code(part_one, part_two)
