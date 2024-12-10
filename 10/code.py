from AoCUtils.utils import *

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
DIRS = [UP, DOWN, LEFT, RIGHT]


def part_one():
    return parse(part_two=False)


def part_two():
    return parse(part_two=True)


def parse(part_two=False):
    grid = [
        [int(c) if c != "." else -1 for c in height]
        for height in parse_input("input2.txt" if part_two else "input1.txt")
    ]
    trailheads = []

    for r, row in enumerate(grid):
        for c, ele in enumerate(row):
            if ele == 0:
                trailheads.append((r, c))

    total = 0
    for head in trailheads:
        total += move(grid, head, set(), part_two)
    return total


def move(grid, position, visited, part_two=False):
    if grid[position[0]][position[1]] == 9:
        if part_two:
            return 1
        if position not in visited:
            visited.add(position)
            return 1
        return 0

    height = grid[position[0]][position[1]]

    trail_count = 0
    for dir in DIRS:
        new_pos = add(position, dir)
        if in_bound(grid, new_pos) and grid[new_pos[0]][new_pos[1]] == height + 1:
            trail_count += move(grid, new_pos, visited, part_two)

    return trail_count


def in_bound(grid, position):
    r, c = position[0], position[1]
    return r >= 0 and r < len(grid) and c >= 0 and c < len(grid[0])


def add(pos1, pos2):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])


run_code(part_one, part_two)
