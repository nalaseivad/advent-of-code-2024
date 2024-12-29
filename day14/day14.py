import sys
import re
from functools import reduce


space_width = -1
space_height = -1


def print_space(robots, quadrants = False):
    skip_x, skip_y = -1, -1
    if quadrants:
        skip_x, skip_y = space_width // 2, space_height // 2
    dict = {}
    for robot in robots:
        dict[robot.position] = dict.get(robot.position, 0) + 1
    for y in range(space_height):
        if y == skip_y:
            print()
            continue
        for x in range(space_width):
            if x == skip_x:
                print(" ", end = "")
                continue
            if (x, y) not in dict:
                print(".", end = "")
                continue
            count = dict[(x, y)]
            print(f"{count}", end="")
        print()


def position_to_quadrant(position):
    mid_x, mid_y = space_width // 2, space_height // 2
    x, y = position
    if x < mid_x and y < mid_y: return 0
    if x > mid_x and y < mid_y: return 1
    if x > mid_x and y > mid_y: return 2
    if x < mid_x and y > mid_y: return 3
    return None


def count_robots_in_quadrants(robots):
    counts = [0, 0, 0, 0]
    for robot in robots:
        quadrant = position_to_quadrant(robot.position)
        if quadrant != None:
            counts[quadrant] += 1
    return counts


class robot:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def __repr__(self):
        return f"robot({self.position}, {self.velocity})"


def patrol(robots, num_steps):
    for robot in robots:
        dx, dy = robot.velocity
        for _ in range(num_steps):
            x, y = robot.position
            robot.position = ((x + dx) % space_width, (y + dy) % space_height)


def print_robots(robots):
    for robot in robots:
        print(f"{robot.position} {robot}")


def parse_robot(line):
    match = re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line)
    if match:
        x, y, vx, vy = (int(x) for x in match.groups())
        return robot((x, y), (vx, vy))
    return None


#
# What does the space look like after 100 seconds?
# Calc and return the product of the counts of robots in each quadrant at this time.
#
def part_1(robots):
    #print_robots(robots)
    #rint()
    for _ in range(100):
        # print_space(robots)
        # print()
        patrol(robots, 1)
        #print_space(robots)
        #print()

    print_space(robots)
    print()
    print_space(robots, True)
    return reduce(lambda x, y: x * y, count_robots_in_quadrants(robots))


#
# It turns out that the Christmas Tree shows up when the quadrant counts product is at a minimum.
# I need to think about why this is.
#
def part_2(robots):
    min_score = float("inf")
    time_of_min_score = None
    for second in range(space_width * space_height):
        patrol(robots, 1)
        quadrant_counts = count_robots_in_quadrants(robots)
        score = reduce(lambda x, y: x * y, quadrant_counts)
        #print(f"{second=},{score=},{quadrant_counts=}")
        if score < min_score:
            print(f"{second}: {score}")
            min_score = score
            time_of_min_score = second + 1
    return time_of_min_score


#
# Print the space at a given point in time
#
def part_3(robots):
    for second in range(space_width * space_height):
        patrol(robots, 1)
        if second == 7131:  # Show me the Xmas tree!
            print_space(robots)
            break
    return 3


def process_file(file_path, fn):
    global space_width, space_height
    space_width, space_height = 101, 103
    if re.match(r"^test\-", file_path):
        space_width, space_height = 11, 7

    robots = []
    with open(file_path, "r") as lines:
        for line in (raw_line.rstrip("\n") for raw_line in lines):
            robot = parse_robot(line)
            robots.append(robot)
    print(fn(robots))


if len(sys.argv) != 3:
    print(f"Usage: python3 {sys.argv[0]} <part> <file_path>")
    exit(1)

part = sys.argv[1]
file_path = sys.argv[2]

# part = "1"
# file_path = "/Users/adavies/src/github/nalaseivad/advent-of-code-2024/day14/test-input.txt"

if part == "1":
    process_file(file_path, part_1)
elif part == "2":
    process_file(file_path, part_2)
elif part == "3":
    process_file(file_path, part_3)
else:
    print("Unknown part")
    exit(1)
