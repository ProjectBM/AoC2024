import heapq
import re
from AoCUtils.utils import *

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

DIRS = [UP, DOWN, LEFT, RIGHT]

# Change for real input vs example
MAX_ROWS = 71  # 7
MAX_COLS = 71  # 7
BYTES_FALLEN = 1024  # 12
END = (70, 70)  # (6, 6)


def part_one():
    bytes = [
        tuple(map(int, re.findall(r"-?\d+", line)))[::-1]
        for line in parse_input("input1.txt")
    ]

    grid = [["."] * MAX_COLS for _ in range(MAX_ROWS)]
    drop_standard_bytes(grid, bytes)

    cost_so_far, _ = dijkstra(grid, (0, 0), END)
    return cost_so_far[END]


def part_two():
    bytes = [
        tuple(map(int, re.findall(r"-?\d+", line)))[::-1]
        for line in parse_input("input2.txt")
    ]

    grid = [["."] * MAX_COLS for _ in range(MAX_ROWS)]

    for i in range(len(bytes)):
        drop_single_byte(grid, bytes[i])
        cost_so_far, _ = dijkstra(grid, (0, 0), END)

        if END not in cost_so_far:
            return bytes[i][::-1]
    return None


def drop_standard_bytes(grid, bytes):
    for i in range(BYTES_FALLEN):
        drop_single_byte(grid, bytes[i])


def drop_single_byte(grid, byte):
    grid[byte[0]][byte[1]] = "#"


def dijkstra(grid, start, end):
    frontier = [(0, start)]
    cost_so_far = {start: 0}
    visited_from = {start: None}

    while len(frontier) != 0:
        c_prio, c_pos = heapq.heappop(frontier)

        if c_pos == end:
            break

        for neighbor in neighbors(grid, c_pos):
            n_pos = neighbor
            new_cost = c_prio + 1

            if n_pos not in cost_so_far or new_cost < cost_so_far[n_pos]:
                visited_from[n_pos] = c_pos
                new_priority = new_cost
                cost_so_far[n_pos] = new_cost
                heapq.heappush(frontier, (new_priority, n_pos))

    return cost_so_far, visited_from


def neighbors(grid, pos):
    return filter(
        lambda new_pos: in_bound(grid, new_pos),
        [add(pos, dir) for dir in DIRS],
    )


def in_bound(grid, pos):
    return (
        0 <= pos[0] < MAX_ROWS
        and 0 <= pos[1] < MAX_COLS
        and grid[pos[0]][pos[1]] != "#"
    )


def add(pos1, pos2):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])


def print_grid(grid):
    for row in grid:
        for c in row:
            print(c, end="")
        print()


run_code(part_one, part_two)
