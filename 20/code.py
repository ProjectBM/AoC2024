from collections import Counter, deque
from AoCUtils.utils import *

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

DIRS = [UP, DOWN, LEFT, RIGHT]

GRID = None


SAVE_TIME = 100
MAX_CHEATS = 20


def parse_input(file):
    grid, start, end = [], None, None

    with open(file=file) as file:
        for i, line in enumerate(file):
            if line.strip() == "":
                continue

            line = line.strip().strip("\n")
            grid.append(list(line))

            if "S" in line:
                start = (i, line.find("S"))
            if "E" in line:
                end = (i, line.find("E"))

    return grid, start, end


def part_one():
    global GRID
    GRID, start, end = parse_input("input1.txt")

    saved_times = solve(start, end)
    freq = Counter(saved_times)

    total_cheats = 0
    for k in sorted(freq.keys()):
        print(f"t={k}, freq={freq[k]}")
        if k >= SAVE_TIME:
            total_cheats += freq[k]
    return total_cheats


def part_two():
    global GRID
    GRID, start, end = parse_input("input2.txt")

    saved_times = solve2(start, end)
    freq = Counter(saved_times)

    total_cheats = 0
    for k in sorted(freq.keys()):
        print(f"t={k}, freq={freq[k]}")
        if k >= SAVE_TIME:
            total_cheats += freq[k]
    return total_cheats


def solve(start, end):
    bfs = deque()
    visited = {}
    bfs.append(start)
    time = -1
    saved_times = []

    while bfs:
        pos = bfs.popleft()
        time += 1
        visited[pos] = time

        for neighbor in neighbors(pos):
            saved_time = cheat(visited, pos, neighbor)
            if saved_time != 0:
                saved_times.append(saved_time)

            if (
                in_bound(neighbor)
                and neighbor not in visited
                and GRID[neighbor[0]][neighbor[1]] != "#"
            ):
                bfs.append(neighbor)

        if pos == end:
            return saved_times

    return saved_times


def solve2(start, end):
    bfs = deque()
    visited = {}
    bfs.append(start)
    time = -1
    saved_times = []

    while bfs:
        pos = bfs.popleft()
        time += 1
        visited[pos] = time

        saved_times.extend(cheat2(visited, pos))

        for neighbor in neighbors(pos):
            if (
                in_bound(neighbor)
                and neighbor not in visited
                and GRID[neighbor[0]][neighbor[1]] != "#"
            ):
                bfs.append(neighbor)

        if pos == end:
            return saved_times

    return saved_times


def cheat(visited, pos, neighbor):
    cheat_pos = add(neighbor, sub(neighbor, pos))
    neighbor_mark = GRID[neighbor[0]][neighbor[1]] if in_bound(neighbor) else None
    cheat_mark = GRID[cheat_pos[0]][cheat_pos[1]] if in_bound(cheat_pos) else None

    if neighbor_mark == None or cheat_mark == None:
        return 0

    if neighbor_mark != "#":
        return 0

    if cheat_mark == "#":
        return 0

    if cheat_pos not in visited:
        return 0

    return visited[pos] - (visited[cheat_pos] + 2)


def cheat2(visited, pos):
    bfs = deque()
    cheat_visited = set()

    bfs.append(pos)
    cheat_visited.add(pos)

    saved_times = []
    cheat_time = 0

    while cheat_time < MAX_CHEATS:
        n = len(bfs)
        for _ in range(n):
            cheat_pos = bfs.popleft()

            for cheat_neighbor in neighbors(cheat_pos):
                if in_bound(cheat_neighbor) and cheat_neighbor not in cheat_visited:
                    mark = GRID[cheat_neighbor[0]][cheat_neighbor[1]]

                    if mark != "#" and cheat_neighbor in visited:
                        saved_time = visited[pos] - (
                            visited[cheat_neighbor] + cheat_time + 1
                        )
                        if saved_time > 0:
                            saved_times.append(saved_time)

                    cheat_visited.add(cheat_neighbor)
                    bfs.append(cheat_neighbor)
        cheat_time += 1
    return saved_times


def neighbors(pos):
    return [add(pos, dir) for dir in DIRS]


def in_bound(pos):
    r, c = len(GRID), len(GRID[0])
    return 0 <= pos[0] < r and 0 <= pos[1] < c


def add(pos1, pos2):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])


def sub(pos1, pos2):
    return (pos1[0] - pos2[0], pos1[1] - pos2[1])


run_code(part_one, part_two)
