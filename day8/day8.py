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


def prune_out_of_bounds(coordinates_pair, grid):
    # print(f"check_bounds: {coordinates_pair=}")
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0
    return [(r, c) for (r, c) in coordinates_pair if r >= 0 and r < num_rows and c >=0 and c < num_cols]


def calc_antinodes(antenna_coordinates_pair, grid):
    print(f"calc_antinodes: {antenna_coordinates_pair=}")
    (r1, c1), (r2, c2) = antenna_coordinates_pair
    dr, dc = abs(r2 - r1), abs(c2 - c1)
    if r1 < r2:
        if c1 > c2:
            #    #
            #   1
            #  2
            # #
            return prune_out_of_bounds(((r1 - dr, c1 + dc), (r2 + dr, c2 - dc)), grid)
        else:
            # #
            #  1
            #   2
            #    #
            return prune_out_of_bounds(((r1 - dr, c1 - dc), (r2 + dr, c2 + dc)), grid)
    else:
        if c1 > c2:
            #    #
            #   2
            #  1
            # #
            return prune_out_of_bounds(((r1 + dr, c1 - dc), (r2 - dr, c2 + dc)), grid)
        else:
            # #
            #  2
            #   1
            #    #
            return prune_out_of_bounds(((r1 + dr, c1 + dc), (r2 - dr, c2 - dc)), grid)


def part_1(grid):
    print_grid(grid)
    print()
    antinodes = set()
    
    antennas = defaultdict(list)
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == '.': continue
            antennas[cell].append((r, c))

    for name, antenna_coordinates_list in antennas.items():
        for antenna_coordinates_pair in combinations(antenna_coordinates_list, 2):
            antinodes_coordinates_list = calc_antinodes(antenna_coordinates_pair, grid)
            grid2 = make_empty_grid(grid)
            for (r, c) in antenna_coordinates_pair:
                grid2[r][c] = name
            for (r, c) in antinodes_coordinates_list:
                grid[r][c] = "#"
                grid2[r][c] = "#"
                antinodes.add((r, c))
            print_grid(grid2)
            print()
            
    print_grid(grid)
    return len(antinodes)


def part_2(equations):
    return 2


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
