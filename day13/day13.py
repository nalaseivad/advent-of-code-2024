import sys
import re
import math


def print_machine(machine):
    a_dx, a_dy, b_dx, b_dy, prize_x, prize_y = machine
    print(f"{a_dx=},{a_dy=},{b_dx=},{b_dy=},{prize_x=},{prize_y=}")


def print_solution(solution):
    num_a, num_b = solution
    print(f"{num_a=},{num_b=}")


def is_whole_number(n):
    if n < 0: return False
    if not isinstance(n, (int, float)): return False
    delta = n - int(n)
    close = math.isclose(delta, 1 if delta > 0.5 else 0, abs_tol=1e-3)
    return close


#
# We need to find positive whole numbers num_a and num_b such that ...
#
# (num_a * a_dx) + (num_b * b_dx) = prize_x
# (num_a * a_dy) + (num_b * b_dy) = prize_y
#
# So ...
#   num_a + (num_b * b_dx / a_dx) = prize_x / a_dx
#   num_a + (num_b * b_dy / a_dy) = prize_y / a_dy
#
#   (num_b * b_dx / a_dx) - (num_b * b_dy / a_dy) = (prize_x / a_dx) - (prize_y / a_dy)
#   num_b * ((b_dx / a_dx) - (b_dy / a_dy)) = (prize_x / a_dx) - (prize_y / a_dy)
#
#   num_b = ((prize_x / a_dx) - (prize_y / a_dy)) / ((b_dx / a_dx) - (b_dy / a_dy))
#   num_a = (prize_x / a_dx) - (num_b * b_dx / a_dx)
#
def solve_machine(machine):
    a_dx, a_dy, b_dx, b_dy, prize_x, prize_y = machine
    num_b = ((prize_x / a_dx) - (prize_y / a_dy)) / ((b_dx / a_dx) - (b_dy / a_dy))
    num_a = (prize_x / a_dx) - (num_b * b_dx / a_dx)
    if not (is_whole_number(num_a) and is_whole_number(num_b)):
        return None
    return (round(num_a), round(num_b))


def part_n(machines, fn):
    total_cost = 0
    for machine in machines:
        fn(machine)
        solution = solve_machine(machine)
        if solution:
            num_a, num_b = solution
            cost = (3 * num_a) + num_b
            total_cost += cost
            print_machine(machine)
            print_solution(solution)
            print()
    return total_cost


def part_1(machines):
    return part_n(machines, lambda machine: None)


def part_2(machines):
    def fn(machine):
        machine[4] += 10_000_000_000_000
        machine[5] += 10_000_000_000_000
    return part_n(machines, fn)


def parse_machine(machine_spec):
    machine = []
    pattern = r";Button A: X\+(\d+), Y\+(\d+);Button B: X\+(\d+), Y\+(\d+);Prize: X=(\d+), Y=(\d+)"
    match = re.match(pattern, machine_spec)
    if match:
        for value in match.groups():
            machine.append(int(value))
    return machine


def process_file(file_path, fn):
    machines = []
    machine_spec = ""
    with open(file_path, "r") as lines:
        for line in (raw_line.rstrip("\n") for raw_line in lines):
            if len(line) == 0:
                machine = parse_machine(machine_spec)
                machines.append(machine)
                machine_spec = ""
                continue
            machine_spec += ";" + line
    machine = parse_machine(machine_spec)
    machines.append(machine)
    print(fn(machines))


if len(sys.argv) != 3:
    print(f"Usage: python3 {sys.argv[0]} <part> <file_path>")
    exit(1)

part = sys.argv[1]
file_path = sys.argv[2]

# part = "1"
# file_path = "/Users/adavies/src/github/nalaseivad/advent-of-code-2024/day13/test-input.txt"

if part == "1":
    process_file(file_path, part_1)
elif part == "2":
    process_file(file_path, part_2)
else:
    print("Unknown part")
    exit(1)
