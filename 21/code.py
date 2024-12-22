from enum import Enum
from functools import cache
from AoCUtils.utils import *
import itertools


UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

DIRS = [UP, DOWN, LEFT, RIGHT]

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
    numeric_codes = [int(code[:-1]) for code in codes]
    max_robots = 2
    complexity = 0
    for i, code in enumerate(codes):
        print(code)
        code = solve(Type.NUMERIC, max_robots, 0, tuple(code))
        print(f"{len(code)} * {numeric_codes[i]}")
        complexity += len(code) * numeric_codes[i]

    return complexity


def part_two():
    codes = parse_input("input2.txt")
    numeric_codes = [int(code[:-1]) for code in codes]
    max_robots = 25
    complexity = 0
    for i, code in enumerate(codes):
        print(code)
        code = solve(Type.NUMERIC, max_robots, 0, tuple(code))
        print(f"{len(code)} * {numeric_codes[i]}")
        complexity += len(code) * numeric_codes[i]

    return complexity


@cache
def solve(type: Type, max_iter, iter, code):
    if iter > max_iter:
        return code

    current = get_key(type, "A")

    combined_code = ()
    for c in code:
        new = get_key(type, c)
        moves = get_movements(current, new)
        illegal_move = get_illegal_moves(type, current, new)
        # print(type, c, current, new, moves, list(illegal_moves))
        current = new

        shortest_code = None
        for perm in set(itertools.permutations(moves)):
            if perm == illegal_move:
                continue
            perm += ("A",)
            solved_perm = solve(Type.DIRECTIONAL, max_iter, iter + 1, perm)

            if shortest_code == None:
                shortest_code = solved_perm
            elif len(solved_perm) < len(shortest_code):
                shortest_code = solved_perm
        combined_code += shortest_code

    return combined_code


def get_key(type: Type, c):
    if type == Type.NUMERIC:
        return NUMERIC[c]
    return DIRECTIONAL[c]


def get_movements(current, target):
    movements = []

    diff = sub(target, current)
    x, y = diff[0], diff[1]

    if x > 0:
        movements.append("v" * x)
    elif x < 0:
        movements.append("^" * abs(x))

    if y > 0:
        movements.append(">" * y)
    elif y < 0:
        movements.append("<" * abs(y))

    return "".join(movements)


def get_illegal_moves(type, current, target):
    diff = sub(target, current)
    x, y = diff[0], diff[1]

    if type == Type.NUMERIC:
        if target[0] != 3 and current[0] == 3 and target[1] == 0:
            movements = []

            if y > 0:
                movements.append(">" * y)
            elif y < 0:
                movements.append("<" * abs(y))
            movements.append("^" * abs(x))
            return tuple("".join(movements))
        if target[0] == 3 and current[0] != 3 and current[1] == 0:
            movements = []
            movements.append("v" * abs(x))

            if y > 0:
                movements.append(">" * y)
            elif y < 0:
                movements.append("<" * abs(y))
            return tuple(("".join(movements)))
    elif type == Type.DIRECTIONAL:
        if target[0] != 0 and current[0] == 0 and target[1] == 0:
            movements = []

            if y > 0:
                movements.append(">" * y)
            elif y < 0:
                movements.append("<" * abs(y))
            movements.append("v" * abs(x))
            return tuple(("".join(movements)))
        if target[0] == 0 and current[0] != 0 and current[1] == 0:
            movements = []
            movements.append("^" * abs(x))

            if y > 0:
                movements.append(">" * y)
            elif y < 0:
                movements.append("<" * abs(y))
            return tuple(("".join(movements)))
    return ""


def sub(pos1, pos2):
    return (pos1[0] - pos2[0], pos1[1] - pos2[1])


run_code(part_one, part_two)
