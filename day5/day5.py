import sys
from functools import cmp_to_key

#
# This is our compare function for ordering based on the rules
#
def in_order(n, m):
    return rules.get((n, m), 0)


def update_is_in_order(update, rules):
    for n in range(len(update)):
        for m in range(n + 1, len(update)):
            if in_order(update[n], update[m]) != -1:   # if not in order based on the rules
                return False
    return True


def part_1(updates):
    total = 0
    for update in updates:
        if update_is_in_order(update, rules):
            # Add middle element of the update list
            total += update[len(update) // 2]         # // is integer division with truncation
    return total


def part_2(updates):
    total = 0
    for update in updates:
        if not update_is_in_order(update, rules):
            update.sort(key=cmp_to_key(in_order))     # Sort in-place using our compare function
            total += update[len(update) // 2]
    return total


def part_n(file_path, fn):
    updates = []
    with open(file_path, "r") as lines:
        for row in (line.rstrip("\n") for line in lines):
            if row == "": break
            n, m = [int(x) for x in row.split("|")]
            # Save the rules in a way that we can use them as a compare function for ordering
            rules[(n, m)] = -1
            rules[(m, n)] = 1
        for row in (line.rstrip("\n") for line in lines):
            if row == "": continue
            updates.append([int(x) for x in row.split(",")])
    print(fn(updates))


rules = {}

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
