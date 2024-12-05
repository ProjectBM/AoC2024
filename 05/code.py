import bisect
from AoCUtils.utils import *


def part_one():
    input = parse_input("input1.txt")
    rules, updates = [], []

    for line in input:
        if "|" in line:
            nums = line.split("|")
            rules.append(((int(nums[0])), int(nums[1])))
        else:
            updates.append([int(num) for num in line.split(",")])
    rules = sorted(rules)

    total = 0
    for update in updates:
        is_valid = True
        for i in range(len(update)):
            if not is_valid:
                break
            for j in range(i + 1, len(update)):
                p = (update[i], update[j])
                idx = bisect.bisect_left(rules, p)
                if rules[idx] != p:
                    is_valid = False
                    break
        if is_valid:
            total += update[len(update) // 2]

    return total


def part_two():
    input = parse_input("input2.txt")
    rules, updates = [], []

    for line in input:
        if "|" in line:
            nums = line.split("|")
            rules.append(((int(nums[0])), int(nums[1])))
        else:
            updates.append([int(num) for num in line.split(",")])
    rules = sorted(rules)

    total = 0
    for update in updates:
        corrected_update = correct_update(rules, update.copy())
        if update != corrected_update:
            total += corrected_update[len(corrected_update) // 2]
    return total


def correct_update(rules, update):
    for i in range(len(update)):
        for j in range(i + 1, len(update)):
            p = (update[i], update[j])
            idx = bisect.bisect_left(rules, p)
            if rules[idx] != p:
                update[i], update[j] = update[j], update[i]
                return correct_update(rules, update)
    return update


run_code(part_one, part_two)
