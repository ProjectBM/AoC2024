from AoCUtils.utils import *
from collections import defaultdict


def part_one():
    left_list = []
    right_list = []

    lines = parse_input("input1.txt")
    for line in lines:
        split_line = line.split("   ")
        left_list.append(int(split_line[0]))
        right_list.append(int(split_line[1]))

    left_list = sorted(left_list)
    right_list = sorted(right_list)

    total = 0
    for i in range(len(left_list)):
        total += abs(left_list[i] - right_list[i])
    return total


def part_two():
    left_list = []
    right_list = defaultdict(int)

    lines = parse_input("input1.txt")
    for line in lines:
        split_line = line.split("   ")
        left_list.append(int(split_line[0]))
        right_list[int(split_line[1])] += 1

    total = 0
    for id in left_list:
        total += id * right_list[id]
    return total


run_code(part_one, part_two)
