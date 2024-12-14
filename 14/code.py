from functools import reduce
from operator import mul
from AoCUtils.utils import *
import re

# Change for puzzle input vs example input
WIDTH = 101
HEIGHT = 103

# Don't use for part 2
TIME = 100


def part_one():
    p, v = [], []
    for line in parse_input("input1.txt"):
        nums = list(map(int, re.findall(r"-?\d+", line)))
        p.append((nums[0], nums[1]))
        v.append((nums[2], nums[3]))

    quadrant_counts = [0] * 4
    viz_pts = []
    for i in range(len(p)):
        px, py, vx, vy = p[i][0], p[i][1], v[i][0], v[i][1]
        res = solve(TIME, px, py, vx, vy)
        viz_pts.append(res)

        quadrant_index = get_quadrant(res[0], res[1])
        if quadrant_index is not None:
            quadrant_counts[get_quadrant(res[0], res[1])] += 1

    # viz(viz_pts)
    return reduce(mul, quadrant_counts)


def part_two():
    p, v = [], []
    for line in parse_input("input2.txt"):
        nums = list(map(int, re.findall(r"-?\d+", line)))
        p.append((nums[0], nums[1]))
        v.append((nums[2], nums[3]))

    for j in range(1000000):
        viz_pts = set()
        for i in range(len(p)):
            px, py, vx, vy = p[i][0], p[i][1], v[i][0], v[i][1]
            res = solve(j, px, py, vx, vy)
            viz_pts.add(res)

        # Find pattern
        for m_x, m_y in viz_pts:
            is_tree = True
            for k in range(4):
                left_x, left_y = m_x - (k + 1), m_y + (k + 1)
                right_x, right_y = m_x + (k + 1), m_y + (k + 1)
                if (left_x, left_y) not in viz_pts or (right_x, right_y) not in viz_pts:
                    is_tree = False
                    break
            if is_tree:
                viz_tree(viz_pts)
                return j
    return None


def get_quadrant(x, y):
    width_quad, height_quad = WIDTH // 2, HEIGHT // 2

    if x < width_quad and y < height_quad:
        return 0
    if x > width_quad and y < height_quad:
        return 1
    if x < width_quad and y > height_quad:
        return 2
    if x > width_quad and y > height_quad:
        return 3
    return None


def viz(pts):
    grid = []
    for i in range(HEIGHT):
        grid.append([])
        for _ in range(WIDTH):
            grid[i].append(".")

    for pt in pts:
        v = grid[pt[1]][pt[0]]
        if v == ".":
            grid[pt[1]][pt[0]] = "1"
        else:
            grid[pt[1]][pt[0]] = str(int(v) + 1)
    pprint(grid)


def viz_tree(pts):
    grid = []
    for i in range(HEIGHT):
        grid.append([])
        for _ in range(WIDTH):
            grid[i].append(".")
    for pt in pts:
        v = grid[pt[1]][pt[0]]
        if v == ".":
            grid[pt[1]][pt[0]] = "*"

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            print(grid[i][j], end="")
        print()


def solve(t, px, py, vx, vy):
    return ((px + (vx * t)) % WIDTH, (py + (vy * t)) % HEIGHT)


run_code(part_one, part_two)
