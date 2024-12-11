from collections import defaultdict, deque
import multiprocessing.queues
from AoCUtils.utils import *
import multiprocessing
import sys

# 1
# 2024
# 20 24
# 2 0 2 4
# 4096 1 4096
sys.setrecursionlimit(100000)

TIME_P1 = 25
TIME_P2 = 25
SEED_ROUNDS = 10

MAX_THREADS = 15

DEBUG = False


class Node:
    def __init__(self, value, depth, parent):
        self.value = value
        self.initial_depth = depth
        self.len_by_depth = defaultdict(int)
        self.parent = parent
        self.children = []

        self.len_by_depth[depth] = 1

    def set_children(self, children):
        self.children = children

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        return f"Value: {self.value}, Lens: {self.len_by_depth}"


def part_one():
    stones = [(int(stone), 0) for stone in parse_input("input1.txt")[0].split()]

    for i in range(TIME_P1):
        new_stones = []
        for stone, time in stones:
            new_stones.extend(rules(stone, time))
        stones = new_stones
    return len(stones)


def part_two():
    stones = [(int(stone), 0) for stone in parse_input("input2.txt")[0].split()]
    seeds = seed_inputs()
    print("Seeds Done")

    debug_count = 0
    skip_counter = 0
    total = 0
    for stone, time in stones:
        queue = deque()
        queue.append((stone, time))

        while queue:
            new_stone, new_time = queue.pop()
            if new_time >= TIME_P2:
                print("What the f")
                return total
            skip_count, transformed_stones = fast_rules(new_stone, new_time, seeds)
            total += skip_count
            skip_counter += skip_count
            queue.extend(transformed_stones)
            debug_count += 1

            if debug_count % 100000 == 0:
                print(
                    f"Debug Counter: {debug_count}, queue size: {len(queue)}, skip_counter: {skip_counter}"
                )

    return total


def fast_rules(stone, time, seeds):
    if stone in seeds:
        clock = min(SEED_ROUNDS, TIME_P2 - time) - 1
        if time + clock + 1 >= TIME_P2:
            return (len(seeds[stone][clock]), [])
        return (
            0,
            [
                (future_stone, time + clock + 1)
                for future_stone, _ in seeds[stone][clock]
            ],
        )

    transformed_stones = rules(stone, time)
    if time + 1 >= TIME_P2:
        return (len(transformed_stones), [])
    return (0, transformed_stones)


def seed_inputs():
    seeds = {i: [] for i in range(10)}

    for seed in seeds.keys():
        seed_stones = [(seed, 0)]
        new_stones = []
        for i in range(SEED_ROUNDS):
            for stone, _ in seed_stones:
                new_stones.extend(rules(stone, i))
            seed_stones = new_stones
            new_stones = []
            seeds[seed].append(seed_stones)

    if DEBUG:
        for seed in seeds.keys():
            print(f"seed={seed}, {seeds[seed]}")

    return seeds


def rules(stone, time):
    if stone == 0:
        return [(1, time + 1)]
    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        return [
            (int(stone_str[: len(stone_str) // 2]), time + 1),
            (int(stone_str[len(stone_str) // 2 :]), time + 1),
        ]
    return [(stone * 2024, time + 1)]


def rules_to_nodes(stones, depth, parent: Node):
    nodes = []
    for stone in stones:
        nodes.append(Node(stone, depth, parent))
        parent.add_child(nodes[-1])
    return nodes


def part_two_trees():
    stones = list(map(int, parse_input("input2.txt")[0].split()))
    memo = {}

    skipped_total = 0
    total = 0
    for stone in stones:
        root = Node(stone, -1, Node(-1, -1, None))
        bfs = deque()
        bfs.append(root)

        skipped_counter = 0
        not_skipped_counter = 0

        for i in range(TIME_P2):
            for _ in range(len(bfs)):
                parent_node: Node = bfs.popleft()
                if parent_node.value in memo:
                    # print(f"Hit Parent Value of: {parent_node.value}")
                    memo_node: Node = memo[parent_node.value]
                    if TIME_P2 - i + 10 <= i - memo_node.initial_depth:
                        # print(
                        #     f"Skipping...{TIME_P2} - {i} <= {i} - {memo_node.initial_depth} with entry { memo_node.len_by_depth[
                        #     memo_node.initial_depth + (TIME_P2 - i)
                        # ]}"
                        # )
                        # print(memo_node.len_by_depth)
                        skipped_total += memo_node.len_by_depth[
                            memo_node.initial_depth + (TIME_P2 - i)
                        ]
                        skipped_counter += 1
                        continue
                else:
                    memo[parent_node.value] = parent_node

                not_skipped_counter += 1
                children_nodes = rules_to_nodes(
                    rules(parent_node.value), i, parent_node
                )
                bfs.extend(children_nodes)

                back_track_node = parent_node
                while back_track_node.parent != None:
                    back_track_node.len_by_depth[i] += len(children_nodes)
                    back_track_node = back_track_node.parent

            # if i % 5 == 0 or i == TIME_P2 - 1:
            print(
                f"Iteration {i} for stone {stone}. Skipped={skipped_counter}, NotSkipped={not_skipped_counter}"
            )
        total += len(bfs)
    print(total, skipped_total, skipped_counter, not_skipped_counter)
    return total + skipped_total


def part_two_threaded():
    stones = list(map(int, parse_input("input2.txt")[0].split()))

    for i in range(TIME_P2):
        print(i, len(stones))
        distribution = len(stones) // MAX_THREADS
        threads = []

        with multiprocessing.Manager() as manager:
            thread_res = manager.list()
            for i in range(MAX_THREADS):
                thread = multiprocessing.Process(
                    target=thread_fn,
                    args=(
                        thread_res,
                        (
                            stones[i * distribution : (i + 1) * distribution]
                            if i != MAX_THREADS - 1
                            else stones[i * distribution :]
                        ),
                    ),
                )
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()

            stones = []
            for res in thread_res:
                stones += res

            if i > 40:
                time.sleep(3)

    return len(stones)


def thread_fn(res, stones):
    new_stones = []
    for stone in stones:
        new_stones.extend(rules(stone))
    res.append(new_stones)


run_code(part_one, part_two)
