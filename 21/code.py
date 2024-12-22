from enum import Enum
from functools import cache
import math
from AoCUtils.utils import *


UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

NUMERIC = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}

DIRECTIONAL = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}


class Type(Enum):
    NUMERIC = 0
    DIRECTIONAL = 1


def part_one():
    codes = parse_input("input1.txt")
    return parts(codes, 2)


def part_two():
    codes = parse_input("input2.txt")
    return parts(codes, 25)


def parts(codes, max_robots):
    numeric_codes = [int(code[:-1]) for code in codes]
    complexity = 0

    for j, code in enumerate(codes):
        # print(code)
        total_len = 0
        for i in range(len(code)):
            total_len += solve_char(
                Type.NUMERIC, max_robots, 0, "A" if i == 0 else code[i - 1], code[i]
            )
        # print(f"{total_len} * {numeric_codes[j]}")
        complexity += total_len * numeric_codes[j]

    return complexity


@cache
def solve_char(type: Type, max_iter, iter, current, dest):
    if iter > max_iter:
        return 1

    current_key = get_key(type, current)
    dest_key = get_key(type, dest)
    possible_moves = get_movements(type, current_key, dest_key)

    min_len = math.inf
    for move in possible_moves:
        move_len = 0
        for i in range(len(move)):
            move_len += solve_char(
                Type.DIRECTIONAL,
                max_iter,
                iter + 1,
                "A" if i == 0 else move[i - 1],
                move[i],
            )
        min_len = min(min_len, move_len)
    return min_len


def get_key(type: Type, c):
    if type == Type.NUMERIC:
        return NUMERIC[c]
    return DIRECTIONAL[c]


def get_movements(type, current, target):
    if current == target:
        return ["A"]
    diff = sub(target, current)
    x, y = diff[0], diff[1]

    x_moves, y_moves = "", ""
    if x > 0:
        x_moves += "v" * x
    elif x < 0:
        x_moves += "^" * abs(x)

    if y > 0:
        y_moves += ">" * y
    elif y < 0:
        y_moves += "<" * abs(y)

    illegal_moves = get_illegal_moves(type, current, target) + "A"
    first_moves, second_moves = x_moves + y_moves + "A", y_moves + x_moves + "A"

    if first_moves == second_moves:
        return [first_moves]
    if first_moves == illegal_moves:
        return [second_moves]
    if second_moves == illegal_moves:
        return [first_moves]
    return [first_moves, second_moves]


# Ugly
def get_illegal_moves(type, current, target):
    diff = sub(target, current)
    x, y = diff[0], diff[1]
    movements = ""

    if type == Type.NUMERIC:
        if target[0] != 3 and current[0] == 3 and target[1] == 0:
            if y > 0:
                movements += ">" * y
            elif y < 0:
                movements += "<" * abs(y)
            movements += "^" * abs(x)
            return movements
        if target[0] == 3 and current[0] != 3 and current[1] == 0:
            movements += "v" * abs(x)
            if y > 0:
                movements += ">" * y
            elif y < 0:
                movements += "<" * abs(y)
            return movements
    elif type == Type.DIRECTIONAL:
        if target[0] != 0 and current[0] == 0 and target[1] == 0:
            if y > 0:
                movements += ">" * y
            elif y < 0:
                movements += "<" * abs(y)
            movements += "v" * abs(x)
            return movements
        if target[0] == 0 and current[0] != 0 and current[1] == 0:
            movements += "^" * abs(x)
            if y > 0:
                movements += ">" * y
            elif y < 0:
                movements += "<" * abs(y)
            return movements
    return ""


def sub(pos1, pos2):
    return (pos1[0] - pos2[0], pos1[1] - pos2[1])


run_code(part_one, part_two)
