from collections import Counter, defaultdict
from AoCUtils.utils import *


TIME_P1 = 25
TIME_P2 = 75


def part_one():
    return solve("input1.txt", TIME_P1)


def part_two():
    return solve("input2.txt", TIME_P2)


def solve(file_name, time_limit):
    stones = list(map(int, parse_input(file_name)[0].split()))

    total = 0
    for stone in stones:
        counter = Counter([stone])
        tmp_counter = defaultdict(int)
        for i in range(time_limit):
            for k, v in counter.items():
                transformed_stones = rules(k)
                for transformed_stone in transformed_stones:
                    tmp_counter[transformed_stone] += v
            counter = tmp_counter
            tmp_counter = defaultdict(int)
        for k, v in counter.items():
            total += v
    return total


def rules(stone):
    if stone == 0:
        return [1]
    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        return [
            int(stone_str[: len(stone_str) // 2]),
            int(stone_str[len(stone_str) // 2 :]),
        ]
    return [stone * 2024]


run_code(part_one, part_two)
