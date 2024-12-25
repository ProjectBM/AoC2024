from AoCUtils.utils import *


def part_one():
    input = parse_input("input1.txt")
    locks, keys = [], []

    c_key_lock = [0] * 5
    is_lock = False
    for i in range(len(input)):
        if i % 7 == 0:
            c_key_lock = c_key_lock = [0] * 5
            is_lock = True if "#" in input[i] else False
            continue
        if i % 7 == 6:
            if is_lock:
                locks.append(c_key_lock)
            else:
                keys.append(c_key_lock)
            continue

        for idx, c in enumerate(input[i]):
            if c == "#":
                c_key_lock[idx] += 1

    return count_pairs(locks, keys)


def part_two():
    print("There is no part 2 :D")
    return


def count_pairs(locks, keys):
    no_overlap_count = 0
    for lock in locks:
        for key in keys:
            if not does_overlap(lock, key):
                no_overlap_count += 1
    return no_overlap_count


def does_overlap(lock, key):
    for i in range(len(lock)):
        if lock[i] + key[i] > 5:
            return True
    return False


run_code(part_one, part_two)
