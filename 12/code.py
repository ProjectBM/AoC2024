from AoCUtils.utils import *
from collections import deque

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

DIRS = [UP, DOWN, LEFT, RIGHT]


def part_one():
    return flood_fill(is_part_one=True)


def part_two():
    return flood_fill(is_part_one=False)


def flood_fill(is_part_one):
    grid = [
        [c for c in line]
        for line in parse_input("input1.txt" if is_part_one else "input2.txt")
    ]
    bfs = deque()
    coords = {(i, j) for j in range(len(grid[0])) for i in range(len(grid))}

    solution = 0
    total_area = 0

    while len(coords) > 0:
        # Select Coord
        corner_count, perimeter_count = 0, 0

        start = next(iter(coords))
        bfs.append(start)
        visited = set()

        # Flood Fill
        while len(bfs) != 0:
            coord = bfs.popleft()
            if coord in visited:
                continue

            visited.add(coord)
            coords.remove(coord)

            corner_count += count_corners(grid, coord)

            for dir in DIRS:
                new_pos = add_pos(coord, dir)
                if in_bound(grid, new_pos) and new_pos not in visited:
                    if grid[new_pos[0]][new_pos[1]] == grid[coord[0]][coord[1]]:
                        bfs.append(new_pos)
                    else:
                        perimeter_count += 1
                if not in_bound(grid, new_pos):
                    perimeter_count += 1

        print(
            f"Area of type {grid[start[0]][start[1]]} is {len(visited)} with corner {corner_count} and perimeter of {perimeter_count}. Total area so far {total_area}"
        )
        total_area += len(visited)
        if is_part_one:
            solution += len(visited) * perimeter_count
        else:
            solution += len(visited) * corner_count
    return solution


def count_corners(grid, pos):
    found_corners = set()
    plot_type = grid[pos[0]][pos[1]]

    up, down, left, right = (
        add_pos(pos, UP),
        add_pos(pos, DOWN),
        add_pos(pos, LEFT),
        add_pos(pos, RIGHT),
    )

    up_right, up_left, down_right, down_left = (
        add_pos(up, RIGHT),
        add_pos(up, LEFT),
        add_pos(down, RIGHT),
        add_pos(down, LEFT),
    )

    ### Interior Corners
    # |_
    if not is_same_type(grid, plot_type, up) and not is_same_type(
        grid, plot_type, right
    ):
        found_corners.add(up_right)

    # _|
    if not is_same_type(grid, plot_type, up) and not is_same_type(
        grid, plot_type, left
    ):
        found_corners.add(up_left)

    # 7
    if not is_same_type(grid, plot_type, left) and not is_same_type(
        grid, plot_type, down
    ):
        found_corners.add(down_left)

    # F
    if not is_same_type(grid, plot_type, right) and not is_same_type(
        grid, plot_type, down
    ):
        found_corners.add(down_right)

    ### Exterior Corners
    # |_
    if (
        is_same_type(grid, plot_type, up)
        and is_same_type(grid, plot_type, right)
        and not is_same_type(grid, plot_type, up_right)
    ):
        found_corners.add(up_right)

    # _|
    if (
        is_same_type(grid, plot_type, up)
        and is_same_type(grid, plot_type, left)
        and not is_same_type(grid, plot_type, up_left)
    ):
        found_corners.add(up_left)

    # 7
    if (
        is_same_type(grid, plot_type, down)
        and is_same_type(grid, plot_type, left)
        and not is_same_type(grid, plot_type, down_left)
    ):
        found_corners.add(down_left)

    # F
    if (
        is_same_type(grid, plot_type, down)
        and is_same_type(grid, plot_type, right)
        and not is_same_type(grid, plot_type, down_right)
    ):
        found_corners.add(down_right)

    return len(found_corners)


def is_same_type(grid, plot_type, pos):
    if not in_bound(grid, pos):
        return False
    return plot_type == grid[pos[0]][pos[1]]


def in_bound(grid, pos):
    r, c = pos[0], pos[1]
    return r >= 0 and r < len(grid) and c >= 0 and c < len(grid[0])


def add_pos(pos1, pos2):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])


run_code(part_one, part_two)
