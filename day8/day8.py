import sys
from collections import defaultdict
from itertools import combinations


def print_grid(grid):
    for row in grid:
        for cell in row:
            print(cell, end = '')
        print()


def make_empty_grid(grid):
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0
    grid2 = []
    for row in grid:
        grid2.append(['.'] * num_cols)
    return grid2


def project_antinodes(start_r, start_c, dr, dc, dir_r, dir_c, num_rows, num_cols, num_projections):
    result = []
    n = 1
    while True:
        r, c = start_r + dir_r * n * dr, start_c + dir_c * n * dc
        if r < 0 or r >= num_rows or c < 0 or c >= num_cols: break
        result.append((r, c))
        if n == num_projections: break
        n = n + 1
    return result


def calc_antinodes(part, antenna_coordinates_pair, grid):
    print(f"calc_antinodes: {antenna_coordinates_pair=}")
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0

    (r1, c1), (r2, c2) = antenna_coordinates_pair
    dr, dc = abs(r2 - r1), abs(c2 - c1)
    
    result = []

    # For part 1 we want to only project one antinode either side of the aligned pair of antennas
    # For part 2 we project out to the edges of the grid
    num_projections = 1 if part == 1 else -1
    
    # For part 2 we also consider the antennas to be antinodes
    if part == 2: result.extend(antenna_coordinates_pair)

    if r1 < r2:
        if c1 > c2:
            #    #
            #   1
            #  2
            # #
            result.extend(project_antinodes(r1, c1, dr, dc, -1, 1, num_rows, num_cols, num_projections))
            result.extend(project_antinodes(r2, c2, dr, dc, 1, -1, num_rows, num_cols, num_projections))
        else:
            # #
            #  1
            #   2
            #    #
            result.extend(project_antinodes(r1, c1, dr, dc, -1, -1, num_rows, num_cols, num_projections))
            result.extend(project_antinodes(r2, c2, dr, dc, 1, 1, num_rows, num_cols, num_projections))
    else:
        if c1 > c2:
            #    #
            #   2
            #  1
            # #
            result.extend(project_antinodes(r1, c1, dr, dc, 1, -1, num_rows, num_cols, num_projections))
            result.extend(project_antinodes(r2, c2, dr, dc, -1, 1, num_rows, num_cols, num_projections))
        else:
            # #
            #  2
            #   1
            #    #
            result.extend(project_antinodes(r1, c1, dr, dc, 1, 1, num_rows, num_cols, num_projections))
            result.extend(project_antinodes(r2, c2, dr, dc, -1, -1, num_rows, num_cols, num_projections))

    return result


def calc(grid, part):
    print_grid(grid)
    print()
    antinodes = set()

    antennas = defaultdict(list)
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == ".":
                continue
            antennas[cell].append((r, c))

    for name, antenna_coordinates_list in antennas.items():
        for antenna_coordinates_pair in combinations(antenna_coordinates_list, 2):
            antinodes_coordinates_list = calc_antinodes(part, antenna_coordinates_pair, grid)
            grid2 = make_empty_grid(grid)
            for r, c in antenna_coordinates_pair:
                grid2[r][c] = name
            for r, c in antinodes_coordinates_list:
                grid2[r][c] = grid[r][c] = "#"
                antinodes.add((r, c))
            print_grid(grid2)
            print()

    print_grid(grid)
    return len(antinodes)


def part_1(grid):
    return calc(grid, 1)


def part_2(grid):
    return calc(grid, 2)


def part_n(file_path, fn):
    grid = []
    with open(file_path, "r") as lines:
        for line in lines:
            grid.append(list(line.rstrip("\n")))
    print(fn(grid))


if len(sys.argv) != 3:
    print(f"Usage: python3 {sys.argv[0]} <part> <file_path>")
    exit(1)

part = sys.argv[1]
file_path = sys.argv[2]

if part == "1":
    part_n(file_path, part_1)
elif part == "2":
    part_n(file_path, part_2)
else:
    print("Unknown part")
    exit(1)
