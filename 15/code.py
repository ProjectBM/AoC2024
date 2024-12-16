from AoCUtils.utils import *

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

DIRS = {
    "<": LEFT,
    "^": UP,
    ">": RIGHT,
    "v": DOWN,
}


def parse_input(file):
    grid, ops = [], ""

    is_grid = True
    with open(file=file) as file:
        for line in file:
            if line.strip() == "":
                is_grid = False
                continue

            line = line.strip().strip("\n")
            if is_grid:
                grid.append(list(line))
            else:
                ops += line

    return grid, ops


def part_one():
    return solve(is_part_one=True)


def part_two():
    return solve(is_part_one=False)


def solve(is_part_one):
    grid, ops = parse_input("input1.txt" if is_part_one else "input2.txt")

    if not is_part_one:
        grid = expand_grid(grid)
    start = find_start(grid)

    for op in ops:
        dir = DIRS[op]

        if is_part_one:
            start = move(grid, start, dir)
        else:
            start = move_pt2(grid, start, dir)

    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == ("O" if is_part_one else "["):
                total += 100 * i + j
    return total


def expand_grid(grid):
    new_grid = []

    for i in range(len(grid)):
        new_grid.append([])
        for j in range(len(grid[0])):
            old_tile, new_title = grid[i][j], None

            if old_tile == "#":
                new_title = ["#", "#"]
            elif old_tile == "O":
                new_title = ["[", "]"]
            elif old_tile == ".":
                new_title = [".", "."]
            else:
                new_title = ["@", "."]

            new_grid[-1].extend(new_title)
    return new_grid


def find_start(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "@":
                return (i, j)


def in_bound(grid, pos):
    return grid_get(grid, pos) != "#"


def add(pos1, pos2):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])


def grid_get(grid, pos):
    return grid[pos[0]][pos[1]]


def move(grid, start, dir):
    new_pos = add(start, dir)
    if not in_bound(grid, new_pos):
        return start

    grid_mark = grid_get(grid, new_pos)
    if grid_mark == ".":
        grid[start[0]][start[1]] = "."
        grid[new_pos[0]][new_pos[1]] = "@"
        return new_pos

    # Must be O
    dist = 0
    while grid_mark == "O":
        dist += 1
        new_pos = add(new_pos, dir)
        grid_mark = grid_get(grid, new_pos)

    if grid_mark == "#":
        return start

    # Must be empty space (.)
    grid[new_pos[0]][new_pos[1]] = "O"
    grid[start[0]][start[1]] = "."

    new_pos = add(new_pos, (dir[0] * -dist, dir[1] * -dist))
    grid[new_pos[0]][new_pos[1]] = "@"
    return new_pos


def move_pt2(grid, start, dir):
    new_pos = add(start, dir)
    if not in_bound(grid, new_pos):
        return start

    grid_mark = grid_get(grid, new_pos)
    if grid_mark == ".":
        grid[start[0]][start[1]] = "."
        grid[new_pos[0]][new_pos[1]] = "@"
        return new_pos

    # Must be []
    if dir == LEFT or dir == RIGHT:
        dist = 0
        while grid_mark == "[" or grid_mark == "]":
            dist += 1
            new_pos = add(new_pos, dir)
            grid_mark = grid_get(grid, new_pos)

        if grid_mark == "#":
            return start

        # Must be .
        old_pos = None
        while dist >= 0:
            old_pos = new_pos
            new_pos = add(new_pos, (-dir[0], -dir[1]))
            grid[old_pos[0]][old_pos[1]], grid[new_pos[0]][new_pos[1]] = (
                grid[new_pos[0]][new_pos[1]],
                grid[old_pos[0]][old_pos[1]],
            )
            dist -= 1

        return old_pos

    # Must be UP or DOWN
    if grid_mark == "]":
        swaps = move_vert(grid, add(new_pos, LEFT), new_pos, dir)
        if swaps != []:
            swap_from_list(grid, swaps)
            swap_grid(grid, start, new_pos)
            return new_pos
    if grid_mark == "[":
        swaps = move_vert(grid, new_pos, add(new_pos, RIGHT), dir)
        if swaps != []:
            swap_from_list(grid, swaps)
            swap_grid(grid, start, new_pos)
            return new_pos
    return start


def move_vert(grid, left_bracket, right_bracket, dir):
    new_left, new_right = add(left_bracket, dir), add(right_bracket, dir)

    if not in_bound(grid, new_left) or not in_bound(grid, new_right):
        return []

    left_grid_mark, right_grid_mark = grid_get(grid, new_left), grid_get(
        grid, new_right
    )
    if left_grid_mark == "." and right_grid_mark == ".":
        return [(new_left, left_bracket), (new_right, right_bracket)]

    # Must be [ or ]
    if left_grid_mark == "[" and right_grid_mark == "]":
        swaps = move_vert(grid, new_left, new_right, dir)
        if swaps != []:
            return swaps + [(new_left, left_bracket), (new_right, right_bracket)]
        return swaps

    if left_grid_mark == "]" and right_grid_mark == ".":
        swaps = move_vert(grid, add(new_left, LEFT), new_left, dir)
        if swaps != []:
            return swaps + [(new_left, left_bracket), (new_right, right_bracket)]
        return swaps

    if left_grid_mark == "." and right_grid_mark == "[":
        swaps = move_vert(grid, new_right, add(new_right, RIGHT), dir)
        if swaps != []:
            return swaps + [(new_left, left_bracket), (new_right, right_bracket)]
        return swaps

    # Must be ] [
    left_moves = move_vert(grid, add(new_left, LEFT), new_left, dir)
    right_moves = move_vert(grid, new_right, add(new_right, RIGHT), dir)

    if left_moves != [] and right_moves != []:
        return unique_keep_order(
            left_moves
            + right_moves
            + [(new_left, left_bracket), (new_right, right_bracket)]
        )

    return []


def swap_from_list(grid, swap_list):
    for swap_a, swap_b in swap_list:
        swap_grid(grid, swap_a, swap_b)


def swap_grid(grid, old_pos, new_pos):
    grid[old_pos[0]][old_pos[1]], grid[new_pos[0]][new_pos[1]] = (
        grid[new_pos[0]][new_pos[1]],
        grid[old_pos[0]][old_pos[1]],
    )


def unique_keep_order(lst):
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]


def viz(grid):
    for r in grid:
        for c in r:
            print(c, end="")
        print()


run_code(part_one, part_two)
