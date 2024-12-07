from AoCUtils.utils import *


def part_one():
    input = parse_input("input1.txt")

    equations = []
    for line in input:
        split = line.split(":")
        target = int(split[0])
        numbers = [int(n) for n in split[1].split()]
        equations.append((target, numbers))

    total = 0
    for target, numbers in equations:
        if solve(["+", "*"], target, numbers, 1, numbers[0]):
            total += target
    return total


def part_two():
    input = parse_input("input2.txt")

    equations = []
    for line in input:
        split = line.split(":")
        target = int(split[0])
        numbers = [int(n) for n in split[1].split()]
        equations.append((target, numbers))

    total = 0
    for target, numbers in equations:
        if solve(["+", "*", "||"], target, numbers, 1, numbers[0]):
            total += target
    return total


def solve(operators, target, numbers, idx, current_total):
    if idx >= len(numbers):
        return False

    for op in operators:
        new_total = current_total
        if op == "+":
            new_total += numbers[idx]
        elif op == "*":
            new_total *= numbers[idx]
        elif op == "||":
            new_total = shift_ten(current_total, numbers[idx]) + numbers[idx]

        if new_total == target and idx == len(numbers) - 1:
            return True

        if new_total > target:
            continue

        is_solvable = solve(operators, target, numbers, idx + 1, new_total)

        if is_solvable:
            return True
    return False


def shift_ten(to_shift, with_shift):
    places = 1
    while with_shift >= 10:
        places += 1
        with_shift //= 10
    return to_shift * (10**places)


run_code(part_one, part_two)
