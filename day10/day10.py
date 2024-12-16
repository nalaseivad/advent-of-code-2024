import sys
from collections import defaultdict


def print_map(map):
    for row in map:
        for cell in row:
            print(cell, end="")
        print()


def print_trails(trails):
    for trail in trails:
        print(trail)


def is_valid_move(map, r, c, visited):
    if r < 0 or r >= len(map) or c < 0 or c >= len(map[0]):
        return False
    if (r, c) in visited:
        return False
    return True


def _find_trails(map, trails, visited, trail, target, final_target):
    r, c = trail[-1]
    cell = map[r][c]
    if cell == final_target:
        trails.append(trail[:])
        return
    target = str(int(target) + 1)
    for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        new_r, new_c = r + dr, c + dc
        if not is_valid_move(map, new_r, new_c, visited):
            continue
        new_cell = map[new_r][new_c]
        if new_cell != target:
            continue
        visited.add((new_r, new_c))
        trail.append((new_r, new_c))
        _find_trails(map, trails, visited, trail, target, final_target)
        trail.pop()
        visited.remove((new_r, new_c))


def find_trails(map, start, end):
    trails = []
    for r, row in enumerate(map):
        for c, cell in enumerate(row):
            if cell != start:
                continue
            visited = set()
            visited.add((r, c))
            _find_trails(map, trails, visited, [(r, c)], start, end)
    return trails


def trails_by_start_end(trails):
    result = defaultdict(lambda: defaultdict(list))
    for trail in trails:
        trail_start = trail[0]
        trail_end = trail[-1]
        result[trail_start][trail_end].append(trail)
    return result


def part_1(trails_by_start_end):
    total_score = 0
    for _, trail_ends in trails_by_start_end.items():
        score = len(trail_ends)
        total_score += score
    return total_score


def part_2(trails_by_start_end):
    total_rating = 0
    for _, trail_ends in trails_by_start_end.items():
        for _, trails in trail_ends.items():
            total_rating += len(trails)
    return total_rating


def part_n(file_path, fn):
    map = []
    with open(file_path, "r") as lines:
        for line in lines:
            row = line.rstrip("\n")
            map.append(list(row))
    print(fn(trails_by_start_end(find_trails(map, "0", "9"))))


if len(sys.argv) != 3:
    print(f"Usage: python3 {sys.argv[0]} <part> <file_path>")
    exit(1)

part = sys.argv[1]
file_path = sys.argv[2]

# part = "1"
# file_path = "/Users/adavies/src/github/nalaseivad/advent-of-code-2024/day10/test-input-5.txt"

if part == "1":
    part_n(file_path, part_1)
elif part == "2":
    part_n(file_path, part_2)
else:
    print("Unknown part")
    exit(1)
