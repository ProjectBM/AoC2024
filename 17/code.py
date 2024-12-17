from itertools import batched
import re
from AoCUtils.utils import *

A, B, C = 0, 0, 0


def part_one():
    global A, B, C

    input = parse_input("input1.txt")
    A = list(map(int, re.findall(r"-?\d+", input[0])))[0]
    B = list(map(int, re.findall(r"-?\d+", input[1])))[0]
    C = list(map(int, re.findall(r"-?\d+", input[2])))[0]

    instructions = list(batched(map(int, re.findall(r"-?\d+", input[3])), n=2))
    index = 0

    out = []
    while index < len(instructions):
        op, operand = instructions[index]
        ret = orchestrate(op, operand)

        # jnz
        if op == 3 and ret != None:
            index = ret // 2
        else:
            index += 1

        # out
        if op == 5:
            out.append(str(ret))
    return ",".join(out)


def part_two():
    # Variables: A, B, C
    # (2, 4) B = A % 8
    # (1, 5) B = B ^ 5 (101)
    # (7, 5) C = A // 2**B
    # (1, 6) B = B ^ 6 (110)
    # (0, 3) A = A // 8
    # (4, 3) B = B ^ C
    # (5, 5) Out -> B % 8
    # (3, 0) Nothing -> A == 0, Else -> Loop

    # Simplication:
    # (2, 4) B = A & 111
    # (1, 5) B = B ^ 5
    # (7, 5) C = A >> B
    # (1, 6) B = B ^ 6
    # (0, 3) A = A >> 3
    # (4, 3) B = B ^ C
    # (5, 5) Out -> (((A % 8) ^ 5 ^ 6) ^ (A >> ((A % 8) ^ 5))) % 8
    # (5, 5) Out -> (((A % 8) ^ 3) ^ (A >> ((A % 8) ^ 5))) % 8 (3 LSBs)

    global A, B, C

    input = parse_input("input2.txt")
    A = list(map(int, re.findall(r"-?\d+", input[0])))[0]
    B = list(map(int, re.findall(r"-?\d+", input[1])))[0]
    C = list(map(int, re.findall(r"-?\d+", input[2])))[0]

    instructions = list(batched(map(int, re.findall(r"-?\d+", input[3])), n=2))
    program = list(map(int, re.findall(r"-?\d+", input[3])))
    p_index = len(program) - 1

    solution = 0
    while p_index >= 0:
        for i in range(64):
            tmp = solution * 8 + i  # * 8 == << 3
            A = tmp
            B = 0
            C = 0

            index = 0
            out = []
            while index < len(instructions):
                op, operand = instructions[index]
                ret = orchestrate(op, operand)

                # jnz
                if op == 3 and ret != None:
                    index = ret // 2
                else:
                    index += 1

                # out
                if op == 5:
                    out.append(ret)

            if out[0] == program[p_index]:
                solution = tmp
                p_index -= 1
                break
    return solution


def orchestrate(op, operand):
    match op:
        case 0:
            return adv(operand)
        case 1:
            return bxl(operand)
        case 2:
            return bst(operand)
        case 3:
            return jnz(operand)
        case 4:
            return bxc(operand)
        case 5:
            return out(operand)
        case 6:
            return bdv(operand)
        case 7:
            return cdv(operand)
        case _:
            print(f"Incorrect op: {op}")
            return
    return 1


def adv(operand):
    global A
    A //= 2 ** combo_operand(operand)


def bxl(operand):
    global B
    B ^= operand


def bst(operand):
    global B
    B = combo_operand(operand) % 8


def jnz(operand):
    global A
    if A == 0:
        return

    return operand


def bxc(_):
    global B, C
    B ^= C


def out(operand):
    return combo_operand(operand) % 8


def bdv(operand):
    global A, B
    B = A // 2 ** combo_operand(operand)


def cdv(operand):
    global A, C
    C = A // 2 ** combo_operand(operand)


def combo_operand(operand):
    if 0 <= operand <= 3:
        return operand

    global A, B, C
    match operand:
        case 4:
            return A
        case 5:
            return B
        case 6:
            return C
        case 7:
            print("Combo Operand 7 is not implemented")
            return
        case _:
            print(f"Incorrect Combo Operand: {operand}")
            return


run_code(part_one, part_two)
