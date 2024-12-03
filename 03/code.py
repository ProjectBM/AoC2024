from AoCUtils.utils import *
import re


def part_one():
    return sum(
        [
            int(parsed.split(",")[0][4:]) * int(parsed.split(",")[1][:-1])
            for parsed in re.findall(
                "mul\\([0-9]{1,3},[0-9]{1,3}\\)", "".join(parse_input("input1.txt"))
            )
        ]
    )


def part_two():
    total = 0
    enabled = True
    for mul, do, dont in re.findall(
        "(mul\\([0-9]{1,3},[0-9]{1,3}\\))|(do\\(\\))|(don't\\(\\))",
        "".join(parse_input("input2.txt")),
    ):
        if mul and enabled:
            total += int(mul.split(",")[0][4:]) * int(mul.split(",")[1][:-1])
        elif do:
            enabled = True
        elif dont:
            enabled = False
    return total


run_code(part_one, part_two)
