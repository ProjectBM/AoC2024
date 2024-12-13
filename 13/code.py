from AoCUtils.utils import *

PRIZE_CONST = 10000000000000


def part_one():
    return solution(is_part_one=True)


def part_two():
    return solution(is_part_one=False)


def solution(is_part_one):
    button_a, button_b, prize = [], [], []

    input = parse_input("input1.txt" if is_part_one else "input2.txt")
    for i in range(len(input)):
        line = input[i]
        # Button A
        if i % 3 == 0:
            x_num, y_num = int(line[line.find("X+") + 2 : line.find(",")]), int(
                line[line.find("Y+") + 2 :]
            )
            button_a.append((x_num, y_num))
        # Button B
        elif i % 3 == 1:
            x_num, y_num = int(line[line.find("X+") + 2 : line.find(",")]), int(
                line[line.find("Y+") + 2 :]
            )
            button_b.append((x_num, y_num))
        # Prize
        else:
            x_num, y_num = int(line[line.find("X=") + 2 : line.find(",")]), int(
                line[line.find("Y=") + 2 :]
            )

            if is_part_one:
                prize.append((x_num, y_num))
            else:
                prize.append((x_num + PRIZE_CONST, y_num + PRIZE_CONST))

    tokens = 0
    for i in range(len(prize)):
        axy, bxy, pxy = button_a[i], button_b[i], prize[i]
        a, b = solve(axy, bxy, pxy)
        if a < 0 or b < 0:
            continue

        if is_int(a) and is_int(b):
            tokens += round(a) * 3 + round(b)
    return tokens


def solve(axy, bxy, pxy):
    # System of equations
    # 94a + 22b = 8400
    # 34a + 67b = 5400
    x_1 = (pxy[0] / bxy[0]) * bxy[1]
    x_2 = ((-axy[0]) / bxy[0]) * bxy[1]
    x_3 = (-axy[1]) - (x_2)
    x_4 = x_1 - pxy[1]

    a = x_4 / x_3
    b = (pxy[0] - (axy[0] * a)) / bxy[0]
    return (a, b)


def is_int(num, delta=0.001):
    return abs(num - round(num)) < delta


run_code(part_one, part_two)
