from collections import defaultdict, deque
from AoCUtils.utils import *


def part_one():
    secrets = list(map(int, parse_input("input1.txt")))
    max_secrets = 2000

    total = 0
    for secret in secrets:
        for _ in range(max_secrets):
            secret = gen_secret(secret)
        total += secret
    return total


def part_two():
    secrets = list(map(int, parse_input("input2.txt")))
    max_secrets = 2000
    sequence_with_prices = defaultdict(int)

    for secret in secrets:
        window = deque()
        prev_price = secret % 10
        seen_sequences = set()

        for i in range(max_secrets):
            secret = gen_secret(secret)
            if i < 4:
                window.append(secret % 10 - prev_price)

                if i == 3:
                    sequence_with_prices[tuple(window)] += secret % 10
                    seen_sequences.add(tuple(window))
            else:
                window.popleft()
                window.append(secret % 10 - prev_price)

                if tuple(window) not in seen_sequences:
                    sequence_with_prices[tuple(window)] += secret % 10
                    seen_sequences.add(tuple(window))
            prev_price = secret % 10

    max_bananas = 0
    for sequence, price in sequence_with_prices.items():
        max_bananas = max(max_bananas, price)
    return max_bananas


def gen_secret(secret):
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, secret * 2048))
    return secret


def mix(secret, given):
    return given ^ secret


def prune(secret):
    return secret % 16777216


run_code(part_one, part_two)
