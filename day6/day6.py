import sys


directions = ["^", ">", "v", "<"]
direction_to_delta = { "^" : (-1, 0), ">" : (0, +1), "v" : (+1, 0), "<" : (0, -1) }
delta_to_new_direction = { (-1, 0) : ">", (0, +1) : "v", (+1, 0) : "<", (0, -1) : "^" }


def print_map(map, guard_coords, guard_direction):
    print(f"{guard_coords=}, {guard_direction=}")
    for r, row in enumerate(map):
        for c, cell in enumerate(row):
            print(guard_direction if (r, c) == guard_coords else cell, end="")
        print()
    print()


def patrol_straight(map, guard_coords, guard_direction):
    height = len(map)
    width = len(map[0]) if height > 0 else 0
    r, c = guard_coords
    dr, dc = direction_to_delta[guard_direction]
    while True:
        map[r][c] = "X"
        next_r = r + dr
        next_c = c + dc
        if next_r < 0 or next_r > height - 1 or next_c < 0 or next_c > width - 1:
            return ((r, c), guard_direction, True)
        if map[next_r][next_c] == "#":
            guard_direction = delta_to_new_direction[(dr, dc)]
            return ((r, c), guard_direction, False)
        r, c = next_r, next_c


def patrol(map, start_coords, start_direction):
    # print_map(map, start_coords, start_direction)
    done = False
    new_coords, new_direction = start_coords, start_direction
    while not done:
        (new_coords, new_direction, done) = patrol_straight(map, new_coords, new_direction)
        # print_map(map, new_coords, new_direction)
    return

#
# Look for a loop in the guard's path and return True if one is found, else False
#
def patrol_2(map, start_coords, start_direction):
    seen = set()
    done = False
    new_coords, new_direction = start_coords, start_direction
    while not done:
        (new_coords, new_direction, done) = patrol_straight(map, new_coords, new_direction)
        # Have we visited this 'before block' cell going in the same direction as before?
        if (new_coords, new_direction) in seen:   
            return True   # Yes => loop found
        seen.add((new_coords, new_direction))
    return False


def part_1(map, start_coords, start_direction):
    patrol(map, start_coords, start_direction)
    count = 0
    for row in map:
        for cell in row:
            if cell == "X":
                count += 1
    return count


#
# Brute force search
# Put a new block on each cell that the guard walks on and see if that results in a loop
#
def part_2(map, start_coords, start_direction):
    # Paint the guard's path
    patrol(map, start_coords, start_direction)
    
    # Enumerate all the cells in the guard's path
    loop_block_coords = set()
    for r, row in enumerate(map):
        for c, cell in enumerate(row):
            if cell == "X":
                map[r][c] = "#"
                # Does this result in a loop?
                if patrol_2(map, start_coords, start_direction):
                    # Loop found, save the new block coords
                    loop_block_coords.add((r, c))
                map[r][c] = "X"
    # print(loop_block_coords)
    return len(loop_block_coords)


def part_n(file_path, fn):
    map = []
    start_coords = (0, 0)
    start_direction = ""
    with open(file_path, "r") as lines:
        for r, line in enumerate(lines):
            line = list(line.rstrip("\n"))
            for c, cell in enumerate(line):
                if cell in directions:
                    line[c] = "."
                    start_coords = (r, c)
                    start_direction = cell
            map.append(line)
    print(fn(map, start_coords, start_direction))


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
