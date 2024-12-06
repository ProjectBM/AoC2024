from AoCUtils.utils import *

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


def part_one():
    input = parse_input("input1.txt")
    grid = [[c for c in line] for line in input]

    pos, dir = None, UP
    for i_r, r in enumerate(grid):
        for i_c, c in enumerate(r):
            if c == "^":
                pos = (i_r, i_c)
                break

    visited = set([pos])
    m, n = len(grid), len(grid[0])
    while pos[0] >= 0 and pos[0] < m and pos[1] >= 0 and pos[1] < n:
        new_pos = (pos[0] + dir[0], pos[1] + dir[1])
        if not (
            new_pos[0] >= 0 and new_pos[0] < m and new_pos[1] >= 0 and new_pos[1] < n
        ):
            break

        if grid[new_pos[0]][new_pos[1]] == "#":
            dir = turn_right(dir)
            continue

        pos = new_pos
        visited.add(new_pos)

    return len(visited)


def part_two():
    input = parse_input("input2.txt")
    grid = [[c for c in line] for line in input]

    pos, dir = None, UP
    for i_r, r in enumerate(grid):
        for i_c, c in enumerate(r):
            if c == "^":
                pos = (i_r, i_c)
                break

    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != ".":
                continue

            grid[i][j] = "#"
            if traverse(grid, pos, dir):
                total += 1
            grid[i][j] = "."

    return total


def traverse(grid, pos, dir):
    visited = set([pos])
    m, n = len(grid), len(grid[0])

    already_visited = 0

    while pos[0] >= 0 and pos[0] < m and pos[1] >= 0 and pos[1] < n:
        new_pos = (pos[0] + dir[0], pos[1] + dir[1])
        if not (
            new_pos[0] >= 0 and new_pos[0] < m and new_pos[1] >= 0 and new_pos[1] < n
        ):
            break

        if grid[new_pos[0]][new_pos[1]] == "#":
            dir = turn_right(dir)
            continue

        if new_pos in visited:
            already_visited += 1
            if already_visited >= (len(grid) * len(grid[0]) // 4):
                return True

        pos = new_pos
        visited.add(new_pos)

    return False


def turn_right(dir):
    if dir == UP:
        return RIGHT
    if dir == DOWN:
        return LEFT
    if dir == LEFT:
        return UP
    if dir == RIGHT:
        return DOWN


run_code(part_one, part_two)
