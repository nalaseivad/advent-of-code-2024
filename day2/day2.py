import sys


def test_consecutive_levels(level1, level2, increasing):
    new_increasing = 1 if level2 > level1 else 0
    if increasing == -1: increasing = new_increasing             # Init increasing if first time

    if level1 == level2: return (False, increasing)              # Levels must be strictly increasing or decreasing
    if abs(level2 - level1) > 3: return (False, increasing)      # Levels must differ by no more than 3
    if new_increasing != increasing: return (False, increasing)  # Levels must continue in the same direction as before
    return (True, new_increasing)


def levels_are_safe(levels):
    increasing = -1
    for n, prev_n in zip(levels[1:], levels):
        (safe, increasing) = test_consecutive_levels(prev_n, n, increasing)
        if not safe: return False
    return True


def part_1(levels):
    return levels_are_safe(levels)


#
# Test sub-lists of the levels with each element removed in turn.  The list is safe if any of the sub-lists are safe.
#
def part_2(levels):
    return any(levels_are_safe(levels[:n] + levels[n + 1 :]) for n in range(len(levels)))


def part_n(file_path, fn):
    safe_count = 0
    with open(file_path, "r") as lines:
        for row in (line.rstrip("\n") for line in lines):
            levels = [int(x) for x in row.split()]
            if fn(levels):
                safe_count += 1
    print(safe_count)


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
