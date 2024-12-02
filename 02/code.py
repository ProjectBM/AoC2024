import random
from AoCUtils.utils import *
from collections import defaultdict


def part_one():
    lines = parse_input("input1.txt")
    reports = []
    for line in lines:
        reports.append(line.split())

    safe = 0
    for report in reports:
        is_incr = None
        is_safe = True
        for i in range(len(report) - 1):
            left_report = int(report[i])
            right_report = int(report[i + 1])
            diff = right_report - left_report

            if diff == 0:
                is_safe = False
                break

            if is_incr is None and diff > 0:
                is_incr = True
            elif is_incr is None and diff < 0:
                is_incr = False

            if is_incr is not None and is_incr and diff < 0:
                is_safe = False
                break

            if is_incr is not None and not is_incr and diff > 0:
                is_safe = False
                break

            if abs(diff) < 1 or abs(diff) > 3:
                is_safe = False
                break

        if is_safe:
            safe += 1
    return safe


def part_two():
    reports = [line.split() for line in parse_input("input2.txt")]
    return sum([safe_report(report) or safe_report(report[::-1]) for report in reports])


def safe_report(report):
    is_safe, did_ignore = True, False
    left_ptr, right_ptr = 0, 1

    # Increasing or decrasing majority
    incr_count, decr_count = 0, 0
    for i in random.sample(range(0, len(report) - 2), 3):
        left_report = int(report[i])
        right_report = int(report[i + 1])

        if right_report - left_report > 0:
            incr_count += 1
        elif right_report - left_report < 0:
            decr_count += 1

    is_incr = True if incr_count > decr_count else False

    while right_ptr <= len(report) - 1:
        left_report = int(report[left_ptr])
        right_report = int(report[right_ptr])

        if not safety(left_report, right_report, is_incr):
            if did_ignore:
                is_safe = False
                break

            if right_ptr + 1 <= len(report) - 1:
                if not safety(left_report, int(report[right_ptr + 1]), is_incr):
                    is_safe = False
                    break
                did_ignore = True
                left_ptr = right_ptr
                right_ptr += 1
        left_ptr += 1
        right_ptr += 1
    return is_safe


def safety(left_report, right_report, is_incr):
    diff = right_report - left_report

    if diff == 0:
        return False

    if is_incr and diff < 0:
        return False

    if not is_incr and diff > 0:
        return False

    if abs(diff) < 1 or abs(diff) > 3:
        return False

    return True


run_code(part_one, part_two)
