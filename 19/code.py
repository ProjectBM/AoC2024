from AoCUtils.utils import *
from functools import cache


def part_one():
    input = parse_input("input1.txt")
    patterns, designs = list(map(str.strip, input[0].split(","))), input[1:]

    possible_count = 0
    for design in designs:
        if solve(tuple(patterns), design, 0):
            possible_count += 1
    return possible_count


def part_two():
    input = parse_input("input2.txt")
    patterns, designs = list(map(str.strip, input[0].split(","))), input[1:]

    possible_count = 0
    for design in designs:
        possible_count += solve2(tuple(patterns), design, 0)
    return possible_count


@cache
def solve(patterns, design, design_idx):
    if design_idx >= len(design):
        return True

    is_possible = False
    for pattern in patterns:
        if design.startswith(pattern, design_idx):
            is_possible |= solve(patterns, design, design_idx + len(pattern))
    return is_possible


@cache
def solve2(patterns, design, design_idx):
    if design_idx >= len(design):
        return 1

    is_possible = 0
    for pattern in patterns:
        if design.startswith(pattern, design_idx):
            is_possible += solve2(patterns, design, design_idx + len(pattern))
    return is_possible


run_code(part_one, part_two)
