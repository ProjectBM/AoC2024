from collections import defaultdict, deque
from AoCUtils.utils import *
import heapq

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


def part_one():
    start, end, grid = None, None, []
    for idx, line in enumerate(parse_input("input1.txt")):
        grid.append(list(line))
        if "S" in line:
            start = (idx, line.find("S"))
        if "E" in line:
            end = (idx, line.find("E"))

    cost_so_far, _ = dijkstra(grid, start, end, is_part_one=True)
    return min(cost_so_far[end].values())


def part_two():
    start, end, grid = None, None, []
    for idx, line in enumerate(parse_input("input2.txt")):
        grid.append(list(line))
        if "S" in line:
            start = (idx, line.find("S"))
        if "E" in line:
            end = (idx, line.find("E"))

    cost_so_far, visited_from = dijkstra(grid, start, end, is_part_one=False)
    return viz_and_calc(grid, start, end, cost_so_far, visited_from)


def dijkstra(grid, start, end, is_part_one):
    frontier = [(0, start, RIGHT)]
    cost_so_far = defaultdict(lambda: defaultdict(int))
    visited_from = defaultdict(lambda: defaultdict(set))
    cost_so_far[start][RIGHT] = 0
    visited_from[start][RIGHT] = None

    while len(frontier) != 0:
        c_prio, c_pos, c_dir = heapq.heappop(frontier)

        if is_part_one and c_pos == end:
            break

        for neighbor in neighbors(grid, c_pos, c_dir):
            n_pos, n_dir = neighbor
            new_cost = c_prio + 1 if n_dir == c_dir else c_prio + 1000

            if (
                n_pos not in cost_so_far
                or n_dir not in cost_so_far[n_pos]
                or new_cost <= cost_so_far[n_pos][n_dir]
            ):
                if new_cost == cost_so_far[n_pos][n_dir]:
                    visited_from[n_pos][n_dir].add((c_pos, c_dir))
                else:
                    visited_from[n_pos][n_dir] = set()
                    visited_from[n_pos][n_dir].add((c_pos, c_dir))

                new_priority = new_cost
                cost_so_far[n_pos][n_dir] = new_cost
                heapq.heappush(frontier, (new_priority, n_pos, n_dir))

    return cost_so_far, visited_from


def neighbors(grid, pos, dir):
    return list(
        map(
            lambda x: x if x[1] == dir else (pos, x[1]),
            filter(
                lambda x: in_bound(grid, x[0]),
                [
                    (add(pos, dir), dir),
                    (add(pos, (dir[1], dir[0])), (dir[1], dir[0])),
                    (add(pos, (-dir[1], -dir[0])), (-dir[1], -dir[0])),
                ],
            ),
        )
    )


def in_bound(grid, pos):
    return grid[pos[0]][pos[1]] != "#"


def viz_and_calc(grid, start, end, cost_so_far, visited_from):
    dir_with_cost = min(cost_so_far[end].items(), key=lambda x: x[1])
    c_dir, c_pos = dir_with_cost[0], end
    seats = set()
    seats.add((start, RIGHT))

    bfs = deque()
    bfs.append((c_pos, c_dir))
    while len(bfs) != 0:
        c_pos, c_dir = bfs.popleft()
        seats.add(c_pos)
        pos_and_dirs = visited_from[c_pos][c_dir]

        for new_pos, new_dir in pos_and_dirs:
            grid[new_pos[0]][new_pos[1]] = label(c_pos, new_pos)
            if new_pos != start:
                bfs.append((new_pos, new_dir))

    for row in grid:
        for c in row:
            print(c, end="")
        print("")
    return len(seats)


def label(from_pos, to_pos):
    new_pos = sub(from_pos, to_pos)
    if new_pos == UP:
        return "^"
    if new_pos == DOWN:
        return "v"
    if new_pos == LEFT:
        return "<"
    return ">"


def add(pos1, pos2):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])


def sub(pos1, pos2):
    return (pos1[0] - pos2[0], pos1[1] - pos2[1])


run_code(part_one, part_two)
