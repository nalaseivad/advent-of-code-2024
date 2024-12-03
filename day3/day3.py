import sys
import re


def part_1(text):
    sum_product = 0
    pattern = r"mul\(\s*(\d+)\s*,\s*(\d+)\s*\)"
    matches = re.finditer(pattern, text)
    for match in matches:
        arg1, arg2 = int(match.group(1)), int(match.group(2))
        sum_product += arg1 * arg2
    return sum_product


def part_2(text):
    sum_product = 0
    pattern = r"mul\(\s*(\d+)\s*,\s*(\d+)\s*\)|don't\(\)|do\(\)"
    matches = re.finditer(pattern, text)
    multiply_on = True
    for match in matches:
        token = match.group(0)
        print(f'{token=}')
        if token.startswith("mul"):
            if multiply_on:
                arg1, arg2 = int(match.group(1)), int(match.group(2))
                sum_product += arg1 * arg2
        elif token == "don't()":
            multiply_on = False
        elif token == "do()":
            multiply_on = True
        else:
            raise Exception("Shouldn't happen")
    return sum_product


def part_n(file_path, fn):
    text = ""
    with open(file_path, "r") as lines:
        for row in (line.rstrip("\n") for line in lines):
            text += row
    print(fn(text))


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
