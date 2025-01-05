import sys
import heapq


def count_o(maze):
    return sum(cell == "O" for row in maze for cell in row)


def arrow(maze, r, c, dr, dc):
    cell = maze[r][c]
    if cell in ["S", "E"]:
        return cell
    return {(0, 1): ">", (-1, 0): "^", (0, -1): "<", (1, 0): "v"}[(dr, dc)]


def letter_o(maze, r, c, dr, dc):
    return "O"


def print_path(maze, path, fn):
    for _, r, c, dr, dc in path:
        maze[r][c] = fn(maze, r, c, dr, dc)
    for row in maze:
        print("".join(row))


def print_maze(maze):
    for row in maze:
        print("".join(row))


def find_paths_by_cost(maze, sr, sc):
    pq = [(0, sr, sc, 0, 1, [])]  # We start at (sr, sc) facing East, (dr, dc) = (0, 1)
    seen = set()
    step_cost, turn_cost = 1, 1000
    paths_by_cost = {}

    while pq:
        cost, r, c, dr, dc, path = heapq.heappop(pq)  # Get the element wth the lowest cost
        seen.add((r, c, dr, dc))
        if maze[r][c] == "E":
            # Destination reached, save the path using its cost as a key
            paths_by_cost.setdefault(cost, []).append(path + [(cost, r, c, dr, dc)])

        #
        #         (-1, 0)          turn left: (dr, dc) -> (-dc, dr)
        #            ^
        #  (0, -1) <-|-> (0, 1)
        #            v
        #          (1, 0)          turn right: (dr, dc) -> (dc, -dr)
        #
        nr, nc = r + dr, c + dc
        moves = [
            (cost + step_cost, r + dr, c + dc, dr, dc),               # Step forward
            (cost + turn_cost + step_cost, r - dc, c + dr, -dc, dr),  # Turn left + step forward
            (cost + turn_cost + step_cost, r + dc, c - dr, dc, -dr),  # Turn right + step forward
        ]
        for ncost, nr, nc, ndr, ndc in moves:
            if maze[nr][nc] == "#" or (nr, nc, ndr, ndc) in seen:  # Wall or backtrack -> skip
                continue
            heapq.heappush(pq, (ncost, nr, nc, ndr, ndc, path + [(cost, r, c, ndr, ndc)]))

    return paths_by_cost


def part_1(maze, sr, sc):
    paths_by_cost = find_paths_by_cost(maze, sr, sc)
    min_cost = min(paths_by_cost.keys())
    path = paths_by_cost[min_cost][0]
    print_path(maze, path, arrow)
    return min_cost


def part_2(maze, sr, sc):
    paths_by_cost = find_paths_by_cost(maze, sr, sc)
    min_cost = min(paths_by_cost.keys())
    for path in paths_by_cost[min_cost]:
        print_path(maze, path, letter_o)  # This fn changes path cells in the maze to "O"
        print()
    return count_o(maze)  # Count the number of Os, i.e. count the cells in the union of all paths


def process_file(file_path, fn):
    maze = []
    sr, sc = -1, -1
    with open(file_path, "r") as file:
        for r, row in enumerate(file):
            for c, cell in enumerate(row):
                if cell == "S":
                    sr, sc = r, c
            maze.append(list(row.rstrip()))
    print(fn(maze, sr, sc))


if len(sys.argv) != 3:
    print(f"Usage: python3 {sys.argv[0]} <part> <file_path>")
    exit(1)

part = sys.argv[1]
file_path = sys.argv[2]

# part = "1"
# file_path = "/Users/adavies/src/github/nalaseivad/advent-of-code-2024/day16/test-input.txt"

if part == "1":
    process_file(file_path, part_1)
elif part == "2":
    process_file(file_path, part_2)
else:
    print("Unknown part")
    exit(1)
