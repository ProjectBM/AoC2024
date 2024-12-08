from AoCUtils.utils import *
from collections import defaultdict


def part_one():
    input = parse_input("input1.txt")
    grid = [list(line) for line in input]
    att = defaultdict(list)

    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c != ".":
                att[c].append((i, j))

    antinodes = set()
    for freq, pts in att.items():
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                pt1, pt2 = pts[i], pts[j]

                yd = pt2[1] - pt1[1]
                xd = pt2[0] - pt1[0]

                possible_antis = [
                    (pt1[0] + xd, pt1[1] + yd),
                    (pt2[0] + xd, pt2[1] + yd),
                    (pt1[0] - xd, pt1[1] - yd),
                    (pt2[0] - xd, pt2[1] - yd),
                ]

                for anti in possible_antis:
                    if anti != pt1 and anti != pt2:
                        antinodes.add(anti)
    total = 0
    for x, y in antinodes:
        if not (x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0])):
            total += 1
    return total


def part_two():
    input = parse_input("input2.txt")
    grid = [list(line) for line in input]
    att = defaultdict(list)

    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c != ".":
                att[c].append((i, j))

    antinodes = set()
    for freq, pts in att.items():
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                pt1, pt2 = pts[i], pts[j]

                antinodes.add(pt1)
                antinodes.add(pt2)

                yd = pt2[1] - pt1[1]
                xd = pt2[0] - pt1[0]

                tmp_x, tmp_y = pt1[0], pt1[1]
                while True:
                    tmp_x += xd
                    tmp_y += yd

                    if (
                        tmp_x >= len(grid)
                        or tmp_y >= len(grid[0])
                        or tmp_x < 0
                        or tmp_y < 0
                    ):
                        break
                    antinodes.add((tmp_x, tmp_y))

                tmp_x, tmp_y = pt1[0], pt1[1]
                while True:
                    tmp_x -= xd
                    tmp_y -= yd

                    if (
                        tmp_x >= len(grid)
                        or tmp_y >= len(grid[0])
                        or tmp_x < 0
                        or tmp_y < 0
                    ):
                        break
                    antinodes.add((tmp_x, tmp_y))
    return len(antinodes)


def viz(grid, antinodes):
    for x, y in antinodes:
        if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0]):
            continue
        if grid[x][y] != ".":
            grid[x][y] = "+"
        else:
            grid[x][y] = "#"
    pprint(grid)


run_code(part_one, part_two)
