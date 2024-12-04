from AoCUtils.utils import *

XMAS = "XMAS"
XMAS_R = "SAMX"


def part_one():
    horizontal = parse_input("input1.txt")
    n, m = len(horizontal), len(horizontal[0])

    vertical = [["." for _ in range(n)] for _ in range(m)]
    for i in range(n):
        for j in range(m):
            vertical[j][i] = horizontal[i][j]
    for i in range(m):
        vertical[i] = "".join(vertical[i])

    r, c = n - 1, 0
    diagonal = []
    while True:
        word = ""
        init_r, init_c = r, c

        while r >= 0 and r < n and c >= 0 and c < m:
            word += horizontal[r][c]
            r += 1
            c += 1
        diagonal.append(word)

        if init_r > 0:
            r = init_r - 1
            c = 0
        elif init_r == 0:
            r = 0
            c = init_c + 1

        if r <= 0 and c >= m:
            break

    r, c = n - 1, m - 1
    other_diagonal = []
    while True:
        word = ""
        init_r, init_c = r, c

        while r >= 0 and r < n and c >= 0 and c < m:
            word += horizontal[r][c]
            r += 1
            c -= 1
        other_diagonal.append(word)

        if init_r > 0:
            r = init_r - 1
            c = m - 1
        elif init_r == 0:
            r = 0
            c = init_c - 1

        if r <= 0 and c < 0:
            break

    total = 0
    for line in horizontal:
        total += line.count(XMAS) + line.count(XMAS_R)
    for line in vertical:
        total += line.count(XMAS) + line.count(XMAS_R)
    for line in diagonal:
        total += line.count(XMAS) + line.count(XMAS_R)
    for line in other_diagonal:
        total += line.count(XMAS) + line.count(XMAS_R)
    return total


def part_two():
    horizontal = parse_input("input2.txt")
    n, m = len(horizontal), len(horizontal[0])

    total = 0
    for i in range(n - 2):
        for j in range(m - 2):
            if forward_diag(horizontal, i, j) and backward_diag(horizontal, i, j + 2):
                total += 1
    return total


def forward_diag(grid, i, j):
    try:
        if grid[i][j] == "M":
            if grid[i + 1][j + 1] == "A":
                if grid[i + 2][j + 2] == "S":
                    return True
        if grid[i][j] == "S":
            if grid[i + 1][j + 1] == "A":
                if grid[i + 2][j + 2] == "M":
                    return True
    except Exception as e:
        print("Ignoring exception: " + e)
    return False


def backward_diag(grid, i, j):
    try:
        if grid[i][j] == "M":
            if grid[i + 1][j - 1] == "A":
                if grid[i + 2][j - 2] == "S":
                    return True
        if grid[i][j] == "S":
            if grid[i + 1][j - 1] == "A":
                if grid[i + 2][j - 2] == "M":
                    return True
    except Exception as e:
        print("Ignoring exception: " + e)
    return False


run_code(part_one, part_two)
