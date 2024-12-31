import sys


def expand_line(line):
    expanded_line = []
    for cell in line:
        if cell == "@":
            expanded_line.extend(["@", "."])
        elif cell == "#":
            expanded_line.extend(["#", "#"])
        elif cell == ".":
            expanded_line.extend([".", "."])
        elif cell == "O":
            expanded_line.extend(["[", "]"])
        else:
            raise "This should not happen"
    return expanded_line


def print_map(map):
    for row in map:
        print("".join(row))


def robot_start_coords(map):
    for r, row in enumerate(map):
        for c, cell in enumerate(row):
            if cell == "@":
                return r, c


def calc_answer(map, box_value):
    answer = 0
    for r, row in enumerate(map):
        for c, cell in enumerate(row):
            if cell == box_value:
                answer += (r * 100) + c
    return answer


def try_push_box(map, start_r, start_c, dr, dc):
    to_move = [(start_r, start_c)]

    r, c = start_r, start_c
    nr, nc = r + dr, c + dc
    while True:
        if map[nr][nc] == "#":
            return start_r, start_c
        if map[nr][nc] == ".":
            break
        # map[nr][nc] is a box
        to_move.append((nr, nc))
        r, c = nr, nc
        nr, nc = r + dr, c + dc

    # There's space, move all the boxes
    for r, c in reversed(to_move):
        map[r + dr][c + dc] = map[r][c]
    map[r][c] = "."

    return start_r + dr, start_c + dc


def try_push_box_2(map, start_r, start_c, dr, dc):
    #print(f"try_push_box_2: {start_r=},{start_c=},{dr=},{dc=},")
    to_move = [(start_r, start_c)]

    up_down = True if dc == 0 else False
    #print(f"{up_down=}")
    edge = set()
    edge.add((start_r, start_c))
    r, c = start_r, start_c
    nr, nc = r + dr, c + dc
    can_move = False
    while True:
        can_move = True
        #print(f"{to_move=}")
        if up_down:
            #print(f"{edge=}")
            for (_, ec) in edge:
                #print(f"{nr=},{ec=}, {map[nr][ec]}")
                if map[nr][ec] == "#":
                    return start_r, start_c
                if map[nr][ec] == "[":
                    can_move = False
                    if (nr, ec) not in to_move:
                        to_move.append((nr, ec))
                    if (nr, ec + 1) not in to_move:
                        to_move.append((nr, ec + 1))  # Add the other part of the box
                elif map[nr][ec] == "]":
                    can_move = False
                    if (nr, ec) not in to_move:
                        to_move.append((nr, ec))
                    if (nr, ec - 1) not in to_move:
                        to_move.append((nr, ec - 1))  # Add the other part of the box
        else:
            #print(f"{map[nr][nc]}")
            if map[nr][nc] == "#":
                return start_r, start_c
            if map[nr][nc] == "[":
                can_move = False
                if (nr, nc) not in to_move:
                    to_move.append((nr, nc))
                if (nr, nc + 1) not in to_move:
                    to_move.append((nr, nc + 1))  # Add the other part of the box
            elif map[nr][nc] == "]":
                can_move = False
                if (nr, nc) not in to_move:
                    to_move.append((nr, nc))
                if (nr, nc - 1) not in to_move: 
                    to_move.append((nr, nc - 1))  # Add the other part of the box

        if can_move:
            break

        edge = set()
        edge.update([(_r, _c) for _r, _c in to_move if _r == nr])
        r, c = nr, nc
        nr, nc = r + dr, c + dc

    # There's space, move all the boxes
    for r, c in reversed(to_move):
        map[r + dr][c + dc] = map[r][c]
        map[r][c] = "."

    return start_r + dr, start_c + dc  # Return the new robot position


#
# No need to test map bounds since the edge of the map is all walls ('#')
#
def try_move(map, r, c, move, push_fn):
    dr, dc = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}[move]
    nr, nc = r + dr, c + dc
    if map[nr][nc] == "#":
        return r, c
    if map[nr][nc] == ".":
        map[nr][nc] = "@"
        map[r][c] = "."
        return nr, nc
    # map[nr][nc] is a box, try to push it
    return push_fn(map, r, c, dr, dc)


def part_n(map, moves, move_fn, push_fn, calc_fn):
    start_r, start_c = robot_start_coords(map)
    print(f"{start_r=}, {start_c=}")
    print(f"{moves}\n")
    print_map(map)
    (r, c) = (start_r, start_c)
    for move in moves:
        print(move)
        nr, nc = move_fn(map, r, c, move, push_fn)
        print_map(map)
        r, c = nr, nc
    return calc_fn(map)


def part_1(map, moves):
    return part_n(map, moves, try_move, try_push_box, lambda map: calc_answer(map, "O"))


def part_2(map, moves):
    return part_n(map, moves, try_move, try_push_box_2, lambda map: calc_answer(map, "["))


def process_file(file_path, fn, transform_line_fn):
    map = []
    moves = []
    with open(file_path, "r") as file:
        map_lines, moves_lines = file.read().split("\n\n")
        for line in map_lines.split("\n"):
            map.append(transform_line_fn(list(line)))
        for line in moves_lines.split("\n"):
            moves.extend(list(line))
    print(fn(map, moves))


if len(sys.argv) != 3:
    print(f"Usage: python3 {sys.argv[0]} <part> <file_path>")
    exit(1)

part = sys.argv[1]
file_path = sys.argv[2]

# part = "2"
# file_path = "/Users/adavies/src/github/nalaseivad/advent-of-code-2024/day15/test-input-1.txt"

if part == "1":
    process_file(file_path, part_1, lambda line: line)
elif part == "2":
    process_file(file_path, part_2, expand_line)
else:
    print("Unknown part")
    exit(1)
