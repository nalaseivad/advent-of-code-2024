import sys
from collections import deque


def print_map(map):
    for row in map:
        print("".join(row))


def find_regions(map):
    rows = len(map)
    cols = len(map[0]) if len(map) > 0 else 0
    visited = set()

    # The number of edges is the same as the number of corners
    def calc_num_edges(plots):
        return calc_num_corners(plots)

    def calc_num_corners(plots):
        corner_candidates = set()
        for r, c in plots:
            #                  +-            -+           -           -
            #                  |X|          |X|          |X|         |X|
            #                   -            -            -+         +-
            plot_to_corners = [(-0.5,-0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)]
            for dr, dc in plot_to_corners:
                corner_r, corner_c = r + dr, c + dc
                corner_candidates.add((corner_r, corner_c))
        num_corners = 0
        for corner_r, corner_c in corner_candidates:
            #                           X|             |X           |           |
            #                           -+-           -+-          -+-         -+-
            #                            |             |            |X         X|
            corner_to_neighbor_plots = [(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)]
            neighbors_in_plots = [(corner_r + dr, corner_c + dc) in plots for dr, dc in corner_to_neighbor_plots]
            count = sum(neighbors_in_plots)  # Booleans behave as 1/0 for this sum
            if count == 1:
                # T|F    F|T    F|F    F|F
                # -+- or -+- or -+- or -+-
                # F|F    F|F    F|T    T|F
                num_corners += 1
            elif count == 2:
                #               <---- not a corner ---->
                # T|F    F|T    T|T    F|T    F|F    T|F
                # -+- or -+- or -+- or -+- or -+- or -+-
                # F|T    T|F    F|F    F|T    T|T    T|F

                #                         T|F                         F|T
                #                         -+-                         -+-
                #                         F|T                         T|F
                if neighbors_in_plots in [[True, False, True, False], [False, True, False, True]]:
                    num_corners += 2   # Double corner
            elif count == 3:
                # F|T    T|F    T|T    T|T
                # -+- or -+- or -+- or -+-
                # T|T    T|T    T|F    F|T
                num_corners += 1
        return num_corners

    def calc_perimeter(plots):
        perimeter = 0
        for r, c in plots:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if not (0 <= nr < rows and 0 <= nc < cols) or (nr, nc) not in plots:
                    # The new cell is outside the region.  This is a region edge and so part of the perimeter.
                    perimeter += 1
        return perimeter

    def find_region_from(r, c):
        nonlocal visited  # Need this because we modify a non-local variable
        plant = map[r][c]
        plots = set([(r, c)])
        queue = deque([(r, c)])
        while queue:
            qr, qc = queue.popleft()
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = qr + dr, qc + dc
                if (nr, nc) in visited: continue
                if (0 <= nr < rows and 0 <= nc < cols and map[nr][nc] == plant):
                    plots.add((nr, nc))
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        return {
            "plant": plant,
            "plots": plots,
            "area": len(plots),
            "perimeter": calc_perimeter(plots),
            "num_edges": calc_num_edges(plots)
        }

    regions = []
    for r in range(rows):
        for c in range(cols):
            if (r, c) in visited: continue
            regions.append(find_region_from(r, c))
    return regions


def part_n(map, fn):
    print_map(map)
    print()
    regions = find_regions(map)
    price = 0
    for region in regions:
        price += fn(region)
        print(f"plant = {region['plant']}")
        print(f"plots = {region['plots']}")
        print(f"area = {region['area']}")
        print(f"perimeter = {region['perimeter']}")
        print(f"num_edges = {region['num_edges']}")
        print()
    return price


def part_1(map):
    return part_n(map, lambda region: region["area"] * region["perimeter"])


def part_2(map):
    return part_n(map, lambda region: region["area"] * region["num_edges"])


def process_file(file_path, fn):
    map = []
    with open(file_path, "r") as lines:
        for line in lines:
            row = list(line.rstrip("\n"))
            map.append(row)
    print(fn(map))


if len(sys.argv) != 3:
    print(f"Usage: python3 {sys.argv[0]} <part> <file_path>")
    exit(1)

part = sys.argv[1]
file_path = sys.argv[2]

# part = "1"
# file_path = "/Users/adavies/src/github/nalaseivad/advent-of-code-2024/day12/test-input-2.txt"

if part == "1":
    process_file(file_path, part_1)
elif part == "2":
    process_file(file_path, part_2)
else:
    print("Unknown part")
    exit(1)
